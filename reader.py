import threading
import time
import json
import psycopg2

SELECT_QUERY = "SELECT SENDER_NAME, MESSAGE, SENT_TIME FROM ASYNC_MESSAGES WHERE RECEIVED_TIME " \
                "IS NULL AND SENDER_NAME != %s FOR UPDATE SKIP LOCKED"

UPDATE_QUERY = "UPDATE ASYNC_MESSAGES SET RECEIVED_TIME = timestamp 'epoch'" \
                "+ %s * interval '1 second' WHERE SENDER_NAME = %s " \
                "AND MESSAGE = %s AND SENT_TIME = %s"

def read_db_config(filename):
    """Function to read database configurations from a JSON file"""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def connect_to_databases(configs):
    """Function to create connections to multiple databases"""
    connections = []
    for config in configs:
        connection = psycopg2.connect(
            database=config["database"],
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"]
        )

        connections.append(connection)

    return connections

def fetch_and_update_message(reader_name, connection):
    """Function fetching an dupdating databse rows"""
    cursor = connection.cursor()
    try:
        cursor.execute(SELECT_QUERY, (reader_name,))
        row = cursor.fetchone()
        if row:
            sender_name, message_text, message_time = row
            cursor.execute(UPDATE_QUERY, (time.time(), sender_name, message_text, message_time))
            connection.commit()
            return sender_name, message_text, message_time
        else:
            return None
    finally:
        cursor.close()

class ReaderThread(threading.Thread):
    """Threads for reading"""
    def __init__(self, name, connection):
        threading.Thread.__init__(self)
        self.name = name
        self.connection = connection

    def run(self):
        while True:
            time.sleep(5)
            print(f'Thread {self.name} is idle for 5 seconds')
            message = fetch_and_update_message(self.name, self.connection)
            if message:
                sender_name, message_text, message_time = message
                print(f"Sender {sender_name} sent {message_text} at time {message_time}.")



# Read database configurations from the JSON file
db_configs = read_db_config('db_config.json')

# Connect to multiple databases
connections = connect_to_databases(db_configs)

# Create and start the reader thread
reader_threads = []
for i, connection in enumerate(connections):
    thread_name = f"Reader_{i}"
    reader_thread = ReaderThread(thread_name, connection)
    reader_threads.append(reader_thread)
    reader_thread.start()

# Main thread waits for the reader threads to complete
for thread in reader_threads:
    thread.join()
