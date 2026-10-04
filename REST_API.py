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

@app.route("/")
def catch_all():
    return render_template("homepage.html")



@app.route("/shorten", methods=["POST"])
def shorten_url():
    match request.method:
        case "POST":
            submitted_url = request.form.get('url')
            print(f"sub url: {submitted_url}")
            db_result = parse_URL.process_url(submitted_url)
            if db_result["status"] == "error":
                return render_template("error_page.html", error_message=db_result["message"])
            
            return jsonify(db_result), 201
        


@app.route("/shorten/<string:shortcode>", methods=["GET", "PUT", "DELETE"])
def parse_shortcode(shortcode=None):
    match request.method:
        case "GET":
            results, db_result = db.retrieve_entry(shortcode)
            if db_result["status"] == "error":
                return jsonify(db_result), 400
            
            return jsonify(results), 201
        case "PUT":
            data = request.get_json()
            url = data.get('url')
            db_result = db.update_entry(shortcode, url)
            if db_result["status"] == "error":
                return jsonify(db_result), 400
            
            return f"Updated entry {shortcode} successfully", 201
        case "DELETE":
            db_result = db.delete_entry(shortcode)
            if db_result["status"] == "error":
                return jsonify(db_result), 400
            
            return f"Deleted entry {shortcode} succesfully", 201

