import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",      # put password if you have
    "database": "motorshow_db"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)
