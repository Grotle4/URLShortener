#TODO: might need to refactor code to split api calls and html rendering.
from flask import Flask, request, jsonify, render_template
import parse_URL
import db

app = Flask(__name__, template_folder="templates")

@app.route("/")
@app.route("/<path:path>")
def catch_all():
    return "The requested endpoint doesn't exist.", 404 



# @app.before_request
# def check_method_override():
#     g.effective_method = request.method

#     if request.method == "POST":
#         method = request.form.get("_method", "").upper()
#         if method in {"PUT", "DELETE"}:
#             g.effective_method = method



@app.route("/shorten", methods=["POST", "GET", "PUT", "DELETE"])
def shorten_url():
    match request.method:
        case "POST":
            data = request.get_json()
            submitted_url = data.get('url')
            db_result, short_key = parse_URL.process_url(submitted_url)
            if db_result["status"] == "error":
                #return render_template("error_page.html", error_message=db_result["message"])
                return f"Error: {db_result["message"]}", 404
            
            #return render_template("homepage.html", shortcode=f"Success! Heres your url: shorten.com/{short_key}")
            return f"Success, entry with short code {short_key} has been added!", 200

        


@app.route("/shorten/<string:shortcode>", methods=["GET","PUT","DELETE"])
def parse_shortcode(shortcode=None):
    match request.method:
        case "GET":
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

