from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
import datetime as dt
import os
import random
import string


load_dotenv("keys.env")
KEY = os.getenv("FLASK_KEY")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = KEY
db = SQLAlchemy(app)
Bootstrap(app)


class Urls(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(200), nullable=False)
    short_url = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/', methods=["POST", "GET"])
def main_page():
    if request.method == "GET":
        return render_template('main.html',
                               copyright=dt.datetime.utcnow().strftime("%Y"))
    elif request.method == "POST":
        post_time = dt.datetime.now(dt.timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
        new_long = request.form["long"]
        alr_exist = Urls.query.filter_by(long_url=new_long).first()
        if alr_exist:
            return render_template('main.html',
                                   copyright=dt.datetime.utcnow().strftime("%Y"),
                                   long_url=new_long,
                                   short_url=alr_exist.short_url,
                                   exist=True,
                                   )
        else:
            new_short = "http://127.0.0.1:5000/" + ''.join(random.choices(string.ascii_letters + string.digits, k=3))
            # add scrollbar to get K number for length of short url #
            new_data = Urls(long_url=new_long,
                            short_url=new_short,
                            time=post_time)
            db.session.add(new_data)
            db.session.commit()
            return render_template('main.html',
                                   copyright=dt.datetime.utcnow().strftime("%Y"),
                                   long_url=new_long,
                                   short_url=new_short,
                                   )


@app.route('/<short_url>', methods=["GET"])
def redirect_page(short_url):
    exist = Urls.query.filter_by(short_url=f"http://127.0.0.1:5000/{short_url}").first()
    if exist:
        return redirect(exist.long_url)
    else:
        return redirect(url_for('main_page'))


if __name__ == "__main__":
    app.run(debug=True)
