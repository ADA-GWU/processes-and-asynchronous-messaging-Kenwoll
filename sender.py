import json
import time
import random
import threading
import psycopg2

SENDER_NAME = "Murad"

INSERT_QUERY = "INSERT INTO ASYNC_MESSAGES(SENDER_NAME, MESSAGE, SENT_TIME) " \
                "VALUES(%s, %s,  to_timestamp(%s))"

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

def insert_message(connection, message):
    """Function to insert a record into the table"""
    cursor = connection.cursor()
    try:
        cursor.execute(INSERT_QUERY, (SENDER_NAME, message, time.time()))
        connection.commit()
    finally:
        cursor.close()

# Read database configurations from the JSON file
db_configs = read_db_config('db_config.json')

# Connect to multiple databases
connections = connect_to_databases(db_configs)

def choose_thread_and_insert_message(threads, message):
    chosen_thread = random.choice(threads)
    chosen_connection = chosen_thread.connection
    print(f"{chosen_thread.name} sends message")
    insert_message(chosen_connection, message)

class SenderThread(threading.Thread):
    def __init__(self, name, connection):
        threading.Thread.__init__(self)
        self.name = name
        self.connection = connection

    def run(self):
        while True:
            user_input = input("Enter your message: ")
            choose_thread_and_insert_message(sender_threads, user_input)

sender_threads = []
for i, connection in enumerate(connections):
    thread_name = f"Sender_{i+1}"
    sender_thread = SenderThread(thread_name, connection)
    sender_threads.append(sender_thread)
    sender_thread.start()

# Main thread waits for the sender threads to complete
for thread in sender_threads:
    thread.join()
