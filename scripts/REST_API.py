from flask import Flask, request, jsonify, render_template

"""
This script covers the api functionality to handle requests and store data to a database.
Needs to be able to:
recieve from frontend
Send processed url to seperate script to check if we can generate a unique url code
Then recieve the proper shortend url and send to database for storage.


"""

app = Flask(__name__)

@app.route("/")
def index():
    render_template
    return 0