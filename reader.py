import threading
import time
from utilities.database_utils import *

class ReaderThread(threading.Thread):
    """Threads for reading"""
    def __init__(self, name, connection):
        threading.Thread.__init__(self)
        self.name = name
        self.connection = connection

    def run(self):
        while True:
            time.sleep(3)
            print(f'Thread {self.name} is idle for 3 seconds')
            message = fetch_and_update_message(self.name, self.connection)
            if message:
                sender_name, message_text, message_time = message
                print(f"UPDATE: Sender {sender_name} sent {message_text} at time {message_time}.")



# Read database configurations from the JSON file
db_configs = read_db_config('config/db_config.json')

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
