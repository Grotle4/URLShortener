from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import parse_URL
import db

app = Flask(__name__, template_folder="templates")
CORS(app, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5500"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route("/")
def catch_all():
    return "The requested endpoint doesn't exist.", 404 


@app.route("/shorten", methods=["POST"])
def shorten_url():
    match request.method:
        case "POST":
            data = request.get_json()
            print(data)
            submitted_url = data.get('url')
            db_result, short_key = parse_URL.process_url(submitted_url)
            if db_result["status"] == "error":
                return f"{db_result["message"]}", 404
            
            return jsonify({"message": f"Success, entry with short code {short_key} has been added!"}), 200

        
@app.route("/shorten/<string:shortcode>", methods=["GET","PUT","DELETE"])
def parse_shortcode(shortcode=None):
    match request.method:
        case "GET":
            print("this runs?")
            results, db_result = db.retrieve_entry(shortcode, False)
            if db_result["status"] == "error":
                return jsonify(db_result), 400
            
            return jsonify(results), 201
        case "PUT":
            data = request.get_json()
            url = data.get('url')
            print(data, url)
            db_result = db.update_entry(shortcode, url)
            if db_result["status"] == "error":
                return jsonify(db_result), 400
            
            return jsonify({"message": f"Updated entry {shortcode} successfully"}), 201
        case "DELETE":
            print("trying to delete")
            print(shortcode)
            db_result = db.delete_entry(shortcode)
            if db_result["status"] == "error":
                return jsonify(db_result), 400
            
            return jsonify({"message": f"Deleted entry {shortcode} succesfully"}), 201
        

@app.route("/shorten/<string:shortcode>/stats", methods=["GET"])
def get_stats(shortcode=None):
    print("statting")
    results, db_result = db.retrieve_entry(shortcode, True)
    if db_result["status"] == "error":
        return jsonify({"message": f"{db_result["message"]}"}), 400
    if shortcode == "":
        return jsonify({"message": f"Failed to fetch"}), 400
        
    
    return jsonify(results), 201



if __name__ == "__main__":
    app.run(port=5000)
