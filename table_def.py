# table_def.py
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///bids.db', echo=True)
Base = declarative_base()

class Users(Base):
	""""""
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True)
	username = Column(String)
	password = Column(String)
	name = Column(String)
	
	def __init__(self, user_name, password, name):
		""""""
		self.username = user_name
		self.password = password
		self.name = name
	
	
 
class Bids(Base):
	""""""
	__tablename__ = "bids"
 
	id = Column(Integer, primary_key=True)
	title = Column(String)
	organization = Column(String)
	currentbid = Column(Integer)
	seller = Column(String)
	pic = Column(String)
	description = Column(String)
	highestbidder = Column(Integer)
	category = Column(String)
 
 
	def __init__(self, title, organization, currentbid, seller, pic, description, bidder, category):
		""""""

		self.title = title
		self.organization = organization
		self.currentbid = currentbid
		self.seller = seller
		self.pic = pic
		self.description = description
		self.highestbidder = bidder
		self.category = category
		
Base.metadata.create_all(engine)
