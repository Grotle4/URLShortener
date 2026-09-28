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
import parse_URL

def create_db_entry(url: str, key: str):
    timestamp = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    db_entry = {
        "url": url,
        "short_code": key,
        "created_at": timestamp,
        "updated_at": timestamp
    }
    connection, cursor = establish_db_connection()
    enter_into_db(db_entry, cursor)


def establish_db_connection():
    load_dotenv()
    db_user = os.getenv("USER")
    db_pass = os.getenv("PASSWORD")
    db_host = os.getenv("HOST")
    db_name = os.getenv("DB")
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )

        if connection.is_connected():
            print("Connected")

            cursor = connection.cursor()
            return connection, cursor
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")



def enter_into_db(entry:dict, cursor, connection):
    entry["short_code"] = check_for_dupes(entry["short_code"], cursor, connection)

    db_query = "INSERT INTO urls (url, shortcode, createdAt, updatedAt) VALUES (%s, %s, %s, %s)"

    values = tuple(entry.values())

    try:
        cursor.execute(db_query, values)
        print(f"Successfully inserted row ID: {cursor.lastrowid}")
        connection.commit()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()
    


def check_for_dupes(short_key: str, cursor, connection):
    db_query = f"SELECT * FROM urls WHERE shortcode = '{short_key}'"
    print("Executing dupe check")
    cursor.execute(db_query)

    results = cursor.fetchall()

    if not results:
        print(f"Entry doesn't exist")
        return short_key
    else:
        print(f"String exists in db")
        new_string = parse_URL.generate_random_string()
        check_for_dupes(new_string, cursor, connection)

def retrieve_entry(key: str):
    db_query = "SELECT * FROM urls WHERE shortcode = %s"
    connection, cursor = establish_db_connection()
    cursor.execute(db_query, (key,))

    try:
        results = cursor.fetchone()
        print(f"Found this entry: {results}")
        return results
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def update_entry(key: str, url: str):
    db_query = "UPDATE urls SET url = %s WHERE shortcode = %s"
    connection, cursor = establish_db_connection()
    try:
        cursor.execute(db_query, (url, key))
        connection.commit()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

