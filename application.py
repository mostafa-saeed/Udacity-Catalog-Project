import sys, os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, CONNECTION_STRING

sys.path.append(os.path.join(os.path.dirname(__file__), 'class'))
from user import User
from item import Item


engine = create_engine(CONNECTION_STRING)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


testUser = User('email=mostafa.saeed543@gmail.com')
session.add(testUser)
session.commit()

print 'Done!'
