"""
This scrip facilitates all database operations for our api. This includes:
POST requests to populate a new entry into our database.
GET requests to search our database for a shortened url entry and then return the original url
PUT requests to search for a shortened url and update the original url

Each entry in our database must contain this dictionary structure:

id: ID in database
url: Original URL
code: Shortened URL Code
date_created: Date Created
last_updated: Last updated

This script will also handle the searching of the database to make sure we do not generate any duplicate ids.

"""
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


def create_db_entry(url: str, key: str):
    timestamp = datetime.now().strftime("%y-%d-%m %H:%M:%S")
    db_entry = {
        "url": url,
        "short_code": key,
        "created_at": timestamp,
        "updated_at": timestamp
    }

def establish_db_connection():
    load_dotenv()
    db_user = os.getenv("USER")
    db_pass = os.getenv("PASSWORD")
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=db_user,
            password=db_pass,
            database="urlshortener"
        )

        if connection.is_connected():
            print("Connected")

            cursor = connection.cursor()

            cursor.execute("SELECT VERSION();")
            db_version = cursor.fetchone(0)
            print(f"Database version: {db_version}")
    except:
        pass

def enter_into_db(entry:dict):
    pass