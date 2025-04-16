# db_config.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Deepa@2000",
        database="chat_app_db"
    )
