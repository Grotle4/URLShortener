#TODO: might need to refactor code to split api calls and html rendering.
from flask import Flask, request, jsonify, render_template
import parse_URL
import db

app = Flask(__name__, template_folder="templates")

@app.route("/")
def catch_all():
    return render_template("homepage.html")



@app.before_request
def check_method_override():
    g.effective_method = request.method

    if request.method == "POST":
        method = request.form.get("_method", "").upper()
        if method in {"PUT", "DELETE"}:
            g.effective_method = method



@app.route("/shorten", methods=["POST", "GET", "PUT", "DELETE"])
def shorten_url():
    match g.effective_method:
        case "POST":
            submitted_url = request.form.get('url')
            db_result, short_key = parse_URL.process_url(submitted_url)
            if db_result["status"] == "error":
                return render_template("error_page.html", error_message=db_result["message"])
            
            return render_template("homepage.html", shortcode=f"Success! Heres your url: shorten.com/{short_key}")
        case "GET":
            shortcode = request.args.get("shortcode")
            results, db_result = db.retrieve_entry(shortcode)
            if db_result["status"] == "error":
                return render_template("error_page.html", error_message=db_result["message"])
            
            return render_template("entry_page.html", id=results[0], url=results[1], shortcode=results[2], created_at=results[3], updated_at=results[4])
        case "PUT":
            shortcode = request.form.get("shortcode")
            url = request.form.get("url")
            db_result = db.update_entry(shortcode, url)
            if db_result["status"] == "error":
                return render_template("error_page.html", error_message=db_result["message"])
            
            return render_template("homepage.html", shortcode=f"Success! Successfully updated entry {shortcode} with URL: {url}")
        case "DELETE":
            shortcode = request.form.get("shortcode")
            db_result = db.delete_entry(shortcode)
            if db_result["status"] == "error":
                return render_template("error_page.html", error_message=db_result["message"])
            
            return f"Deleted entry {shortcode} succesfully", 201


@app.route("/shorten/stats", methods=["GET"])
def get_stats():
    shortcode = request.args.get("shortcode")
    results, db_result = db.retrieve_entry(shortcode)
    if db_result["status"] == "error":
        return render_template("error_page.html", error_message=db_result["message"])
    
    return render_template("entry_page.html", 
                            id=results[0], 
                            url=results[1], 
                            shortcode=results[2], 
                            created_at=results[3], 
                            updated_at=results[4],
                            access_count=f"Number of times accessed: {results[5]}")

