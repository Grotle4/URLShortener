from flask import Flask, request, jsonify, render_template

"""
This script covers the api functionality to handle requests and store data to a database.
Needs to be able to:
recieve from frontend
Send processed url to seperate script to check if we can generate a unique url code
Then recieve the proper shortend url and send to database for storage.


"""

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("homepage.html")

@app.route("/submit", methods=["POST"])
def parse_url():
    submitted_url = request.form.get("url_input")
    print(submitted_url)
    return render_template("processing.html")

@app.route("/return")
def return_home():
    return render_template("homepage.html")