"""
This script covers the api functionality to handle requests and store data to a database.
Needs to be able to:
recieve from frontend
Send processed url to seperate script to check if we can generate a unique url code
Then recieve the proper shortend url and send to database for storage.


"""
from flask import Flask, request, jsonify, render_template
import parse_URL
import db

app = Flask(__name__, template_folder="templates")


@app.route("/shorten", methods=["POST"])
def shorten_url():
    match request.method:
        case "POST":
            #Code here should then process the submitted url and return a shortened one.
            data = request.get_json()
            submitted_url = data.get('url')
            parse_URL.process_url(submitted_url)
            return "URL recieved successfully", 201
        


@app.route("/shorten/<string:shortcode>", methods=["GET", "PUT", "DELETE"])
def parse_shortcode(shortcode=None):
    match request.method:
        case "GET":
                    #Code here should check database for the shortened url.
                    #If stats is used in the API call, then instead return all the information and how many times that url has been accessed.
                    results = db.retrieve_entry(shortcode)
                    return jsonify(results), 201

