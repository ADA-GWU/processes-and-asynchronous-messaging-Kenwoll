import random
import threading
from utilities.database_utils import *

class SenderThread(threading.Thread):
    def __init__(self, name, connection):
        threading.Thread.__init__(self)
        self.name = name
        self.connection = connection

# Read database configurations from the JSON file
db_configs = read_db_config('config/db_config.json')

# Connect to multiple databases
connections = connect_to_databases(db_configs)

# Connect to multiple databases
sender_threads = []
for i, connection in enumerate(connections):
    thread_name = f"Sender_{i+1}"
    sender_thread = SenderThread(thread_name, connection)
    
    sender_threads.append(sender_thread)
    sender_thread.start()

for thread in sender_threads:
    thread.join()

while True:
    message = input("Enter your message: ")
    chosen_thread = random.choice(sender_threads)
    insert_message(chosen_thread.connection, message)
    print(f"{chosen_thread.name} finished query")
    
    flag = input("If you wanna continue press Enter else type 'Exit': ")
    if flag.lower() == "exit":
        break

for thread in sender_threads:
    thread.connection.close()