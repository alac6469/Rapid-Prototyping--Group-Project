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

@app.route('/')
@app.route("/home/")
def landing():
    return render_template('home.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

if __name__ == "__main__":
    app.run(debug=True)

