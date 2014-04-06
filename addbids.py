import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import Bids

engine = create_engine('sqlite:///bids.db', echo=True)

#Create a Session
Session = sessionmaker(bind=engine)
session = Session()

#Create an Artist
#newbid1 = Bids("One week stay in cabin at Breckenridge!", "St. Judes", 45.50, "Joe Smoe", "http://www.raft1.com/wp-content/uploads/2011/03/SCCR_Hawks_Ridge_4.jpg") 
#newbid2 = Bids("iPhone 4", "Feeding America", 320, "Parker Rogers", "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTGuzZFCd5eWW-TIU2PNRgD2xKGqdDTDHzw5DxS8wzPL1B-CyoZ")
newbid1 = Bids("Xbox 360", "Salvation Army", 95.00, "Rabbit Ears", "http://upload.wikimedia.org/wikipedia/commons/f/f3/Xbox-360-arcade.jpg") 
#Add the record to the session object
session.add(newbid1)
#session.add(newbid2)

session.commit()