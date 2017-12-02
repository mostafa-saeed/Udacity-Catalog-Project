import json
import random
import string

from flask import session, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CONNECTION_STRING
from functools import wraps
from models.user import User
from models.item import Item

engine = create_engine(CONNECTION_STRING)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbSession = DBSession()


def generateRandomToken():
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32)
    )


# get categories from items table
def getCategories():
    itemsCategories = (
        dbSession.query(Item).distinct(Item.category)
        .group_by(Item.category, Item.id).all()
    )
    categories = []
    for item in itemsCategories:
        categories.append(str(item.category))
    return categories


def unauthorizedResponse(message):
    response = make_response(json.dumps(message), 401)
    response.headers['Content-Type'] = 'application/json'
    return response


def successResponse(message):
    response = make_response(json.dumps(message), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


# try to find a user in the database using email
# return the user if was found
# or create a new user then return it
def getOrCreateUser(email):
    user = dbSession.query(User).filter_by(email=email).first()
    if user:
        return user
    else:
        newUser = User(email=email)
        dbSession.add(newUser)
        dbSession.commit()
        return dbSession.query(User).filter_by(email=email).first()


# check if the user is logged in
# when updating / deleting items
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            response = unauthorizedResponse('Login is required!')
            return response
        return f(*args, **kwargs)
    return decorated_function
