from flask import Flask, request, render_template

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pprint import pprint

from string import upper
from random import random, shuffle
from copy import deepcopy
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bids.db'
db = SQLAlchemy(app)

app.debug = True

class Bids(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    organization = db.Column(db.String)
    currentbid = db.Column(db.Integer)
    seller = db.Column(db.String)
    pic = db.Column(db.String)

    def __init__(self, title, organization, currentbid, seller, pic):
        self.title = title
        self.organization = organization
        self.currentbid = currentbid
        self.seller = seller
        self.pic = pic


@app.route('/')
@app.route("/home/")
def landing():
    return render_template('home.html')

@app.route('/browse')
def browse():
    bidsData = Bids.query.all()
    return render_template('browse.html', bids = bidsData)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

if __name__ == "__main__":
    app.run(debug=True)

