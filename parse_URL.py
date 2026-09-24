"""
This script facilitates the parsing of our generated url to generate a shortened one.
It will also return this info to the api to then send to database. 
Once completion of the shortened code is done. All data should be formatted into a dictionary to then insert into the database.
"""
import random
import string
import db


def process_url(url: str):
    short_key = generate_random_string()
    print(f"short: {short_key}")

    db.create_db_entry(url, short_key)


def generate_random_string():
    random_sequence = string.ascii_letters + string.digits
    short_key = "".join(random.choices(random_sequence, k=5))
    return short_key



