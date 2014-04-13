from flask import Flask, request, render_template

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pprint import pprint

from string import upper
from random import random, shuffle
from copy import deepcopy
from flask.ext.sqlalchemy import SQLAlchemy
from table_def import Bids, Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bids.db'
db = SQLAlchemy(app)
user = None
app.debug = True
'''
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String)
	password = db.Column(db.String)
	name = db.Column(db.String)
	
	def __init__(self, user_name, password, name):
		self.username = user_name
		self.password = password
		self.name = name
	
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
'''

@app.route('/')
@app.route("/home/")
def landing():
    return render_template('home.html')
@app.route('/echo/', methods = ['POST', 'GET'])
def echo():
	print "hello"
	
@app.route('/browse')
def browse():
    bidsData = Bids.query.all()
    return render_template('browse.html', bids = bidsData)

@app.route('/register')
def register():
	'''if request.method == 'POST':
		user = request.form['username']
		password = request.form['password']
		name = request.form['name']
		print name'''
		
	return render_template('register.html')

@app.route('/signin', methods = ['POST', 'GET'])
def signin():
	
	if request.method == 'POST':
		user = request.form['username']
		password = request.form['password']
		name = request.form['name']
		
		new_user = Users(user, password,name)
		db.session.add(new_user)
		db.session.commit()
		return'data recieved'
	else:
		return render_template('signin.html')

if __name__ == "__main__":
    app.run(debug=True)

