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

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
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


@app.route('/')
@app.route("/home/")
def landing():
    global user
    return render_template('home.html', user = user)
@app.route('/echo/', methods = ['POST', 'GET'])
def echo():
    print "hello"
    
@app.route('/browse')
def browse():
    global user
    bidsData = Bids.query.all()
    return render_template('browse.html', bids = bidsData, user = user)

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

@app.route('/verifyuser', methods = ['POST', 'GET'])
def verifyuser():
    global user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print username
        print password

        #registered_user = session.query(Users).filter(Users.username = username).filter(Users.password = password)

        #registered_user = session.query(Users).filter_by(username = username, password = password)
        
        registered_user = Users.query.filter_by(username = username, password = password).first()
        #registered_user = Users.query.all()
        print registered_user
        if registered_user is None:
            #flash('Username or Password is invalid' , 'error')
            return 'Invalid username or password'
            #return redirect(url_for('login'))
        else:
            user = username
            #flash('Login successful')
            print 'Login successful'
            print user
            return 'Login successful'

@app.route('/profile')
def profile():
    global user
    userBids = Bids.query.filter_by(seller = user)
    
    return render_template('profile.html', user = user, bids = userBids)

@app.route('/create')
def create():
    global user
    return render_template('create.html', user = user)

@app.route('/addbid', methods = ['POST', 'GET'])
def addbid():
    global user
    if request.method == 'POST':
		if user == None:
			return "Please signin"
		#gather reuqest data
		title = request.form['title']
		description = request.form['description']
		organization = request.form['organization']
		currentbid = request.form['startbid']
		pic = request.form['pic']
		seller = user
		#create a new bid and add it to the data base
		new_bid = Bids(title, organization, currentbid, seller, pic)
		db.session.add(new_bid)
		db.session.commit()
		return "Your bid was added"

if __name__ == "__main__":
    app.run(debug=True)

