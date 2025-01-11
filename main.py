from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from flask import session
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import two_factor_auth as two_fa
import userManagement as dbHandler
import validate_and_sanatise as validator


# Code snippet for logging a message
# app.logger.critical("message")

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# Generate a unique basic 16 key: https://acte.ltd/utils/randomkeygen
app = Flask(__name__)
app.secret_key = b"_53oi3uriq9pifpff;apl"
csrf = CSRFProtect(app)


# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["POST", "GET"])
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
    return render_template("/index.html", devtag=devtag)


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")


# example CSRF protected form
@app.route("/signup.html", methods=["POST", "GET"])
def signup():
    errors = {
        'length': False,
        'upper': False,
        'lower': False,
        'number': False,
        'special': False
    }
    if request.method == "POST":
        devtag = validator.sanitize_input(request.form["devtag"])
        password = request.form["password"]
        if dbHandler.userExists(devtag):
            errors['duplicate'] = True
        if len(password) < 8:
            errors['length'] = True
        if not any(char.isupper() for char in password):
            errors['upper'] = True
        if not any(char.islower() for char in password):
            errors['lower'] = True
        if not any(char.isdigit() for char in password):
            errors['number'] = True
        if not any(char in '!@#$%^&*' for char in password):
            errors['special'] = True
        if not any(errors.values()):
            # Password is valid, proceed with signup
            password = validator.hash(password)
            dbHandler.insertUser(devtag, password)
            key = two_fa.get_2fa()
            session["2fa_key"] = key
            session["devtag"] = devtag
            return render_template("/2fa.html", key=key, devtag=devtag)
        else:
            return render_template("/signup.html", errors=errors)

    return render_template("/signup.html", errors=errors)

@app.route("/login.html", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        devtag = validator.sanitize_input(request.form["devtag"])
        password = request.form["password"]
        if not dbHandler.userExists(devtag) or not dbHandler.verifyPassword(devtag, password):
            error = "Incorrect Developer Tag or Password"
        if not error:
            # Successful sign-in
            key = two_fa.get_2fa()
            session["2fa_key"] = key
            session["devtag"] = devtag
            return render_template("/2fa.html", key=key, devtag=devtag)
        else:
            return render_template("/login.html", error=error)
    else:
        return render_template("/login.html")


@app.route("/2fa.html", methods=["POST", "GET"])
def twofa():
    if request.method == "POST":
        key = session.get("2fa_key")
        code = request.form["code"]
        if two_fa.check_2fa(key, code):
            return render_template("/index.html", devtag=session.get('devtag'))
        else:
            return render_template("/2fa.html", error=True, key=key, devtag=session.get('devtag'))
    else:
        return render_template("/2fa.html", key=session.get('2fa_key'), devtag=session.get('devtag'))

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
