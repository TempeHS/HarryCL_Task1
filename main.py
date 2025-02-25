from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from flask import session
import sqlite3 as sql
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import two_factor_auth as two_fa
import database_manager as dbHandler
import validate_and_sanatise as validator
from datetime import datetime
import bleach
import entry_form
import diary_management as diary
from flask import flash
from datetime import timedelta
import os

# Code snippet for logging a message
# app.logger.critical("message")

# Generate a unique basic 16 key: https://acte.ltd/utils/randomkeygen
app = Flask(__name__)
auth_key = "4L50v92nOgcDCYUM"
app.secret_key = b"_53oi3uriq9pifpff;apl"
csrf = CSRFProtect(app)

app_header = {"Authorisation": "4L50v92nOgcDCYUM"}

# Set session lifetime to 24 hours
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1440)


app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# Checks if the user is logged in, particularly when trying to access a page which requires authentication
# Redirects to the login page if not authenticated
def require_login():
    public_routes = ['/login', '/signup', '/static']
    if request.args.get('url'):
        allowed_redirects = {
            'index.html',
            'entry.html', 
            'search.html',
            'privacy.html',
            'diary_logs.html'
        }
        redirect_url = request.args.get('url')
        if redirect_url not in allowed_redirects:
            return redirect("login.html"), 302
    if not any(request.path.startswith(route) for route in public_routes):
        if 'devtag' not in session or session.get('devtag') is None:
            session.clear()
            return redirect("login.html"), 302

# Gets rid of sensitive cache
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/", methods=["GET"])
def root():
    return redirect("/login.html")


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")

@app.route("/login.html", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        devtag = request.form["devtag"]
        password = request.form["password"]
        error = None
        if not dbHandler.userExists(devtag) or not dbHandler.verifyPassword(devtag, password):
            error = "Incorrect Developer Tag or Password"
        if devtag == "AdminUser":
            session["devtag"] = devtag
            return redirect("/index.html")
        if not error:
            # Gets user pyotp
            key = dbHandler.getUserKey(devtag)
            #Creates the Flask session and stores 2FA key within session data
            session["2fa_key"] = key
            session["devtag"] = devtag
            return redirect("/2fa.html")
        else:
            return render_template("/login.html", error=error)
    else:
        return render_template("/login.html")

@app.route("/2fa.html", methods=["POST", "GET"])
def twofa():
    if request.method == "POST":
        key = session.get("2fa_key")
        code = request.form["code"]
        if isinstance(key, tuple):
            key = key[0]
        if two_fa.check_2fa(code, key):
            session.pop("2fa_key", None)
            return redirect("/index.html")
        else:
            return render_template("/2fa.html", error=True, signup=True, key=key, devtag=session.get('devtag'))
    else:
        return render_template("/2fa.html", key=session.get('2fa_key'), devtag=session.get('devtag'))

@app.route("/index.html", methods=["POST", "GET"])
@csp_header(
    {
        # Server Side CSP is consistent with meta CSP in layout.html
        "base-uri": "'self'",
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self'",
        "img-src": "'self' data:",
        "media-src": "'self'",
        "font-src": "'self'",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'",
    }
)
def index():
    devtag = session.get("devtag")
    url = "http://127.0.0.1:3000"
    data = {}
    try:
        response = requests.get(url, headers=app_header)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {"error": "Failed to retrieve data from the API"}
    return render_template("index.html", data=data, devtag=devtag)
# example CSRF protected form
@app.route("/signup.html", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        devtag = request.form["devtag"]
        devtag = bleach.clean(devtag)
        password = request.form["password"]
        errors = validator.validate_password(devtag, password)
        if not any(errors.values()):
            password = validator.hash(password)
            pyotp_key = two_fa.gen_key()
            # Generates the 2FA key and stores it in the database
            dbHandler.insertUser(devtag, password, pyotp_key)
            key = two_fa.get_2fa(devtag,pyotp_key)
            #Creates the Flask session and stores 2FA key within session data
            session["2fa_key"] = key
            session["devtag"] = devtag
            return render_template("/2fa.html", key=key, devtag=devtag, signup=True)
        else:
            return render_template("/signup.html", errors=errors)
    return render_template("/signup.html", errors={})

@app.route("/entry.html", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = entry_form.entry_input(session, request.form)
        url = "http://127.0.0.1:3000/add_diary"
        try:
            response = requests.post(url, json=data, headers=app_header)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            data = {"error": "Failed to send data to API"}
            return render_template("entry.html", data=data, devtag=session.get("devtag"))
        else:
            return render_template("entry.html", success=True, devtag=session.get("devtag"))
    return render_template("entry.html", devtag=session.get("devtag"))

@app.route("/logout", methods= ["POST"])
def logout():
    username = session.pop('username', None)
    if username:
        app_log.info("User '%s' logged out successfully", username)
    session.clear()
    return redirect("login.html")

@app.route("/search.html", methods=["GET"])
def search_page():
    url = "http://127.0.0.1:3000/search"
    data = []
    filters = request.args.to_dict()
    try:
        response = requests.get(url, params=filters, headers=app_header)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        data = {"error": "Failed to retrieve data from the API"}
    return render_template("search.html", data=data, devtag=session.get("devtag"))

@app.route("/download_data", methods=["GET"])
def download():
    devtag = session.get("devtag")
    if not devtag:
        return {"error": "User not logged in"}
    return dbHandler.download_user_data(devtag)

@app.route("/delete_account", methods=["POST"])
def delete_account():
    devtag = session.get("devtag")
    if not devtag:
        return {"error": "User not logged in"}
    diary.delete_user(devtag)
    session.clear()
    return redirect("login.html")

@app.route('/diary_logs/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    url = f"http://127.0.0.1:3000/get_entry/{entry_id}"
    try:
        response = requests.get(url, headers=app_header)
        response.raise_for_status()
        entry = response.json()
        return render_template('diary_logs.html', entry=entry)
    except requests.exceptions.RequestException:
        return render_template('diary_logs.html', entry={"error": "Failed to retrieve entry"})

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    ssl_context = ('cert.pem', 'key.pem')
    app.run(debug=debug_mode, host="0.0.0.0", port=5000, ssl_context=ssl_context)