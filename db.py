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
import validators


def create_db_entry(url: str, key: str):
    timestamp = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    db_entry = {
        "url": url,
        "short_code": key,
        "created_at": timestamp,
        "updated_at": timestamp
    }
    connection, cursor, db_result = establish_db_connection()
    if db_result["status"] == "error":
        return db_result
    db_entry_result, final_result = enter_into_db(db_entry, cursor, connection)
    return db_entry_result, final_result["short_code"]


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
            return connection, cursor, {"status": "success", "message": f"Successfully connected."}
    except mysql.connector.Error as e:
        return connection, cursor, {"status": "error", "message": f"Error connection to database: {e.msg}"}
        



def enter_into_db(entry:dict, cursor, connection):
    entry["short_code"] = check_for_dupes(entry["short_code"], cursor, connection)

    db_query = "INSERT INTO urls (url, shortcode, createdAt, updatedAt) VALUES (%s, %s, %s, %s)"
    
    values = tuple(entry.values())
    if not is_url(values[0]):
        return {"status": "error", "message": "Invalid url provided."}, entry

    try:
        cursor.execute(db_query, values)

        connection.commit()

        return {"status": "success", "message": f"Sucessfully inserted item."}, entry
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return {"status": "error", "message": f"{e.msg}"}, entry
    finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()
    

def check_for_dupes(short_key: str, cursor, connection):
    db_query = f"SELECT * FROM urls WHERE shortcode = '{short_key}'"
    cursor.execute(db_query)

    results = cursor.fetchall()

    if not results:
        return short_key
    else:
        new_string = parse_URL.generate_random_string()
        check_for_dupes(new_string, cursor, connection)


def retrieve_entry(key: str):
    db_query = "SELECT * FROM urls WHERE shortcode = %s"

    connection, cursor, connection_result = establish_db_connection()
    if connection_result["status"] == "error":
        return connection_result

    cursor.execute(db_query, (key,))

    try:
        results = cursor.fetchone()
        if not results:
            return {}, {"status": "error", "message": f"No item found with short code: {key}."}
        else:
            print(f"Found this entry: {results}")
            return results, {"status": "success", "message": "Sucessfully retrieved item."}
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return {}, {"status": "error", "message": f"{e.msg}"}
    
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def is_url(url_string):
    return validators.url(url_string.strip()) is True


def update_entry(key: str, url: str):
    db_query = "UPDATE urls SET url = %s WHERE shortcode = %s"
    connection, cursor = establish_db_connection()
    try:
        if not is_url(url):
            return {"status": "error", "message": "Invalid url provided."}
        
        cursor.execute(db_query, (url, key))
        if cursor.rowcount == 0:
            return {"status": "error", "message": f"No item found with short code: {key}."}
        else:
            connection.commit()
            return {"status": "success", "message": f"Sucessfully updated item {key} with url: {url}."}
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return {"status": "error", "message": f"{e.msg}"}
    
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def delete_entry(key: str):
    db_query = "DELETE FROM urls WHERE shortcode = %s"
    
    connection, cursor = establish_db_connection()
    try:
        cursor.execute(db_query, (key,))
        if cursor.rowcount == 0:
            return {"status": "error", "message": f"No item found with short code: {key}."}
        else:
            connection.commit()
            return {"status": "success", "message": f"Sucessfully deleted item {key}."}
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return {"status": "error", "message": f"{e.msg}"}
    
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
