from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from datetime import datetime as dt
import os


load_dotenv("keys.env")
KEY = os.getenv("FLASK_KEY")

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = KEY

# db = SQLAlchemy(app)
Bootstrap(app)


# class URLS(db.Model):
#     __tablename__ = "urls"
#     id = db.Column(db.Integer, primary_key=True)
#     long_url = db.Column(db.String(200), nullable=False)
#     short_url = db.Column(db.String(200), nullable=False)
#     time = db.Column(db.String(50), nullable=False)
#
#
# db.create_all()


@app.route('/')
def main_page():
    return render_template('main.html', copyright=dt.utcnow().strftime("%Y"))


if __name__ == "__main__":
    app.run(debug=True)


