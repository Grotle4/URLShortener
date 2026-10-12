from flask import Flask, request, jsonify, render_template
import parse_URL
import db

app = Flask(__name__, template_folder="templates")

@app.route("/")
@app.route("/<path:path>")
def catch_all():
    return "The requested endpoint doesn't exist.", 404 


@app.route("/shorten", methods=["POST"])
def shorten_url():
    match request.method:
        case "POST":
            data = request.get_json()
            submitted_url = data.get('url')
            db_result, short_key = parse_URL.process_url(submitted_url)
            if db_result["status"] == "error":
                return f"Error: {db_result["message"]}", 404
            
            return f"Success, entry with short code {short_key} has been added!", 200

        
@app.route("/shorten/<string:shortcode>", methods=["GET","PUT","DELETE"])
def parse_shortcode(shortcode=None):
    match request.method:
        case "GET":
            print("testing if this is pinging.")
            results, db_result = db.retrieve_entry(shortcode, False)
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
        

@app.route("/shorten/<string:shortcode>/stats", methods=["GET"])
def get_stats(shortcode=None):
    results, db_result = db.retrieve_entry(shortcode, True)
    if db_result["status"] == "error":
        return render_template("error_page.html", error_message=db_result["message"])
    
    return jsonify(results), 201

