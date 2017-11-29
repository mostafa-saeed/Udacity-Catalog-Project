import sys, os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from classes.user import User
from classes.item import Item

from database_setup import Base, CONNECTION_STRING

engine = create_engine(CONNECTION_STRING)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


testUser = User(email='mostafa.saeed543@gmail.com')
session.add(testUser)
session.commit()

print 'Done!'
