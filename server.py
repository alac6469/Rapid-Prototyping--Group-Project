from flask import Flask, request, render_template, session
from sqlalchemy import func, desc
from sqlalchemy.sql import label
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pprint import pprint
from datetime import datetime, timedelta
from string import upper
from random import random, shuffle
from copy import deepcopy
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bids.db'
db = SQLAlchemy(app)
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
    description = db.Column(db.String)
    highestbidder = db.Column(db.Integer)
    bidtime = db.Column(db.DateTime)
    category = db.Column(db.String)
    

    def __init__(self, title, organization, currentbid, seller, pic, description, bidder, category, bidtime = None):
        self.title = title
        self.organization = organization
        self.currentbid = currentbid
        self.seller = seller
        self.pic = pic
        self.description = description
        self.highestbidder = bidder
        self.category = category
        self.bidtime = bidtime


@app.route('/')
@app.route("/home/")
def landing():
    if 'user' in session:
        user = session['user']
       
    else:
        
        user = None
    bids = Bids.query.order_by(desc(Bids.bidtime)).limit(5).all()
    return render_template('home.html', user = user, bids = bids)
@app.route('/echo/', methods = ['POST', 'GET'])
def echo():
    print "hello"
    
@app.route('/browse', methods = ['POST', 'GET'])
def browse():
    organizations = None
    cat = None
    title = None
    if 'user' in session:
        user = session['user']
    else:
        user = None
   
    if 'title' in request.args:
        title  = request.args.get('title')
        if title == "":
            title = None
    if 'cat' in request.args:
        cat = request.args.get('cat')
    
        if cat == 'All Categories':
            cat = None
    if 'g' in request.args:
        organizations = request.args.getlist('g')
        orgslist = "organization = '" + organizations.pop() + "'"
        for item in organizations:
            orgslist +=( " or organization ='" + item + "'")
        print orgslist
    if cat != None and title == None and organizations == None: 
        bidsData = Bids.query.filter_by( category = cat).all()  
    elif cat == None and title != None and organizations == None:
        bidsData = Bids.query.filter_by( title = title).all()
    elif cat != None and title != None and organizations == None:
        bidsData = Bids.query.filter_by( category = cat, title = title).all()   
    elif cat != None and title != None and organizations != None:
        bidsData = db.engine.execute("SELECT * FROM bids where " + orgslist + " and category = '" + cat + "' and title = '" + title + "'")
    elif cat == None and title != None and organizations != None:
        bidsData = db.engine.execute("SELECT * FROM bids where " + orgslist +  " and title = '" + title + "'")
    elif cat != None and title == None and organizations != None:
        bidsData = db.engine.execute("SELECT * FROM bids where '" + orgslist + "' and category = '" + cat + "'")
    elif cat == None and title == None and organizations != None:
        bidsData = db.engine.execute("SELECT * FROM bids where " + orgslist)
     
    
    
  
    #if all none
    else: 
        bidsData = Bids.query.all()


   
    return render_template('browse.html', bids = bidsData, user = user,)

@app.route('/register')
def register():
    if 'user' in session:
        user = session['user']
       
    else:
        
        user = None
        
    return render_template('register.html', user = user)

@app.route('/signin', methods = ['POST', 'GET'])
def signin():
    if 'user' in session:
        user = session['user']
       
    else:
        
        user = None
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        name = request.form['name']
    #make sure passwords match
        print "stop 1"
        confirm = request.form['conf']
        if confirm != password:
            return "Passwords Don't match"
        
        #creat a new user and add it them to the data base
        new_user = Users(user, password,name)
        db.session.add(new_user)
        db.session.commit()
        return'data recieved'
    else:
        return render_template('signin.html', user = user)

@app.route('/verifyuser', methods = ['POST', 'GET'])
def verifyuser():
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
            session['user'] = username
            #flash('Login successful')
            print 'Login successful'

            return 'Login successful'

@app.route('/profile')
def profile():
    if 'user' in session:
        user = session['user']

       
    else:
        
        user = None
    userBids = Bids.query.filter_by(seller = user)
    
    return render_template('profile.html', user = user, bids = userBids)

@app.route('/create')
def create():
    if 'user' in session:
        user= session['user']       
    else:
        
        user = None
    return render_template('create.html', user = user)
    
@app.route('/details/<id>')
def details(id = None):
    if 'user' in session:
        user = session['user']
               
    else:
        
        user = None
    bid = Bids.query.filter_by( id = id).first()
    
    return render_template('details.html', user = user, item = bid)
    
@app.route('/addbid', methods = ['POST', 'GET'])
def addbid():
    if 'user' in session:
        user= session['user']

       
    else:
        
        user = None
    if request.method == 'POST':
        if user == None:
            return "Please signin"
        #gather reuqest data
        title = request.form['title']
        description = request.form['description']
        organization = request.form['organization']
        currentbid = request.form['startbid']
        pic = request.form['pic']
        category = request.form['category']
        print category
        seller = user
        #create a new bid and add it to the data base
        new_bid = Bids(title, organization, currentbid, seller, pic,description, currentbid, category, datetime.now() )
        db.session.add(new_bid)
        db.session.commit()
        return "Your bid was added"

@app.route('/updatebid', methods = ['POST', 'GET'])
def updatebid():
    if 'user' in session:
        user = session['user']
       
    else:
        
        user = None
    if request.method == 'POST':
        if user == None:
            return "Please signin"
        bid = int(request.form['bid'])
        id = request.form['id']
        item = Bids.query.filter_by( id = id).first()
        print type(bid)
        print type(item.currentbid)
        
        if bid <= item.currentbid :
            return "Too low"
        else :
            item.currentbid = bid
            item.highestbidder = user
            item.bidtime = datetime.now()
            db.session.commit()
            return " You are the highest bidder!"

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == "__main__":
    app.run(debug=True)

