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