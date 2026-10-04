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

@app.route("/shorten", methods=["POST", "GET", "PUT"])
def shorten_url():
    match request.method:
        case "POST":
            #Code here should then process the submitted url and return a shortened one.
            data = request.get_json()
            submitted_url = data.get('url')
            print(submitted_url)
            return "URL recieved successfully", 201
        case "GET":
            #Code here should check database for the shortened url.
            #If stats is used in the API call, then instead return all the information and how many times that url has been accessed.
            pass
        case "PUT":
            #Code here should check data base for the shortened url code and update with new url
            pass
        case "DELETE":
            #Code here should delete from database base on shortened url code
            pass    