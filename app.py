from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://wndfprpdserrvq:082b370cf8972db8e9d3a624aadfd104e51cb5393605c68cc42ff296ea51eb81@ec2-107-20-198-176.compute-1.amazonaws.com:5432/d3p9cgcamj2bep?sslmode=require'

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Data(db.Model):
    __tablename__ = "survey"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True, nullable=False)
    height_ = db.Column(db.Integer, nullable=False)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=["POST"])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        height=request.form["height_name"]
        if db.session.query(Data).filter(Data.email_==email).count() == 0: 
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            count=db.session.query(Data.height_).count()
            send_email(email, height, average_height, count)
            return render_template("success.html")
    return render_template('index.html', text="That email address has already been used. Please try another!")



if __name__ == "__main__":
    app.debug = True
    app.run()