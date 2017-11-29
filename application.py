from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from classes.user import User
from classes.item import Item

from database_setup import Base, CONNECTION_STRING

engine = create_engine(CONNECTION_STRING)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



from flask import Flask, render_template, request, redirect, jsonify, url_for



app = Flask(__name__)
@app.route('/items/')
def getAllItems():
    items = session.query(Item).all()
    return jsonify(items=[c.serialize for c in items])





app.debug = True
app.run(host='0.0.0.0', port=5000)

#=======================================================================