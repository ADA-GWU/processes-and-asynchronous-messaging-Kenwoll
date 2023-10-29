import psycopg2
import json
import time

_MASTER_NAME = "Murad"

_INSERT_QUERY = "INSERT INTO ASYNC_MESSAGES(SENDER_NAME, MESSAGE, SENT_TIME) " \
                "VALUES(%s, %s,  to_timestamp(%s))"

_SELECT_QUERY = "SELECT SENDER_NAME, MESSAGE, SENT_TIME FROM ASYNC_MESSAGES WHERE RECEIVED_TIME " \
                "IS NULL AND SENDER_NAME != %s FOR UPDATE SKIP LOCKED"

_UPDATE_QUERY = "UPDATE ASYNC_MESSAGES SET RECEIVED_TIME = timestamp 'epoch'" \
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

def insert_message(connection, message):
    """Function to insert a record into the table"""
    cursor = connection.cursor()
    try:
        cursor.execute(_INSERT_QUERY, (_MASTER_NAME, message, time.time()))
        connection.commit()
    finally:
        cursor.close()

def fetch_and_update_message(reader_name, connection):
    """Function fetching an dupdating databse rows"""
    cursor = connection.cursor()
    try:
        cursor.execute(_SELECT_QUERY, (_MASTER_NAME,))
        row = cursor.fetchone()
        if row:
            sender_name, message_text, message_time = row
            cursor.execute(_UPDATE_QUERY, (time.time(), sender_name, message_text, message_time))
            connection.commit()
            return sender_name, message_text, message_time
        else:
            return None
    finally:
        cursor.close()