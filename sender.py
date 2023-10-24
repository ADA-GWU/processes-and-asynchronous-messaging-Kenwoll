import psycopg2
import time

conn = psycopg2.connect(
    database="async_db",
    user="dist_user",
    password="dist_pass_123",
    host="localhost",
    port="6060"
)

def fetch_and_update_message(your_name):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT SENDER_NAME, MESSAGE, SENT_TIME FROM ASYNC_MESSAGES WHERE RECEIVED_TIME IS NULL AND SENDER_NAME != %s FOR UPDATE SKIP LOCKED",
            (your_name,))
        row = cursor.fetchone()
        if row:
            sender_name, message_text, message_time = row
            cursor.execute("UPDATE ASYNC_MESSAGES SET RECEIVED_TIME = timestamp 'epoch' + %s * interval '1 second' WHERE SENDER_NAME = %s AND MESSAGE = %s AND SENT_TIME = %s",
                           (time.time(), sender_name, message_text, message_time))
            conn.commit()
            return sender_name, message_text, message_time
        else:
            return None
    finally:
        cursor.close()
