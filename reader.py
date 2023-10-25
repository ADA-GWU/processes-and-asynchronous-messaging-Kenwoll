"""Python module for enabling threading"""
import threading
import time
import psycopg2

# credentials for my own local testing
conn = psycopg2.connect(
    database="async_db",
    user="dist_user",
    password="dist_pass_123",
    host="localhost",
    port="6060"
)

def fetch_and_update_message(your_name):
    """Function fetching an dupdating databse rows"""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT SENDER_NAME, MESSAGE, SENT_TIME FROM ASYNC_MESSAGES WHERE RECEIVED_TIME " \
                "IS NULL AND SENDER_NAME != %s FOR UPDATE SKIP LOCKED",
            (your_name,))
        row = cursor.fetchone()
        if row:
            sender_name, message_text, message_time = row
            cursor.execute("UPDATE ASYNC_MESSAGES SET RECEIVED_TIME = timestamp 'epoch'" \
                                "+ %s * interval '1 second' WHERE SENDER_NAME = %s " \
                                "AND MESSAGE = %s AND SENT_TIME = %s",
                           (time.time(), sender_name, message_text, message_time))
            conn.commit()
            return sender_name, message_text, message_time
        else:
            return None
    finally:
        cursor.close()

class ReaderThread(threading.Thread):
    """Threads for reading"""
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        while True:
            time.sleep(5)
            print(f'Thread {self.name} is idle for 5 seconds')
            message = fetch_and_update_message(self.name)
            if message:
                sender_name, message_text, message_time = message
                current_time = time.time()
                print(f"Sender {sender_name} sent {message_text} at time {message_time}.")

# Create and start the reader thread
reader_thread = ReaderThread("Some Name")
reader_thread.start()

# Main thread waits for the reader thread to complete
reader_thread.join()

"""
This code currently only create s1 connection to databse and 1 thread for it in
the upcoming day i will change it into multi db connection
"""