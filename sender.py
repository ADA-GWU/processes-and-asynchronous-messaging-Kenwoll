"""Python module for enabling threading"""
import json
import psycopg2

def read_db_config(filename):
    """Function to read database configurations from a JSON file"""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Read database configurations from the JSON file
db_configs = read_db_config('db_config.json')

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

# Connect to multiple databases
connections = connect_to_databases(db_configs)