# table_def.py
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///bids.db', echo=True)
Base = declarative_base()
 
class Bids(Base):
	""""""
	__tablename__ = "bids"
 
	id = Column(Integer, primary_key=True)
	title = Column(String)
	organization = Column(String)
	currentbid = Column(Integer)
	seller = Column(String)
	pic = Column(String)
 
 
	def __init__(self, title, organization, currentbid, seller, pic):
		""""""

		self.title = title
		self.organization = organization
		self.currentbid = currentbid
		self.seller = seller
		self.pic = pic

Base.metadata.create_all(engine)