from flask import Flask, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from short_url import UrlEncoder

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_URI = "sqlite:///" + os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

su = UrlEncoder(alphabet='DEQhd2uFteibPwq0SWBInTpA_jcZL5GKz3YCR14Ulk87Jors9vNHgfaOmMXy6Vx-', block_size=16)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.UnicodeText, unique=True)

    def __init__(self, url):
        self.url = url

    def getname(self):

        return su.enbase(self.id, 1)

    def geturl(self):

        return url_for("get", path=self.getname(), _external=True) + "\n"

def shorten(url):
    existing = URL.query.filter_by(url=url).first()

    if existing:

        return existing.geturl()
    else:
        u = URL(url)
        db.session.add(u)
        db.session.commit()

        return u.geturl()

@app.route("/<path:path>")
def get(path):
    p = os.path.splitext(path)
    id = su.debase(p[0])

    u = URL.query.get(id)
    if u:

        return redirect(u.url)

@app.route("/", methods=["GET", "POST"])
def fhost():
    if request.method == "POST":
        sf = None

        if "shorten" in request.form:

            return shorten(request.form["shorten"])

    return """
<h1>Short your URLS.</h1>

<p>ie:</p>
<p>curl -F'shorten=http://example.com/some/long/url' http://localhost:5000</p>

<br>
<p>Made by ISC School & CodeNoSchool</p>
"""
        
