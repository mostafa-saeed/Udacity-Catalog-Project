from flask import Flask, render_template, request, redirect, jsonify, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, CONNECTION_STRING

from models.user import User
from models.item import Item

engine = create_engine(CONNECTION_STRING)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbSession = DBSession()

import json, random, string

#=======================================================================
def generateRandomToken():
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32)
    )


#=======================================================================

app = Flask(__name__)

# isAuthenticated && isAuthorized
# responses
# Google+ Login

@app.route('/')
@app.route('/catalog/')
def homePage():
    categories = dbSession.query(Item).distinct(Item.category).group_by(Item.category).all()
    print categories

    items = dbSession.query(Item).order_by('-Item.id').limit(10)
    return render_template('home.html',
        categories=categories,
        items=items,
        isAuthenticated=hasattr(session, 'email')
    )

@app.route('/category/<string:categoryName>/')
@app.route('/category/<string:categoryName>/items/')
def getCategory(categoryName):
    items = dbSession.query(Item).filter_by(category=categoryName).all()
    return render_template('category.html',
        items=items,
        isAuthenticated=hasattr(session, 'email')
    )

@app.route('/items/<int:itemID>/')
def getItem(itemID):
    item = dbSession.query(Item).filter_by(id=itemID).one()
    return render_template('item.html',
        item=item,
        isAuthenticated=hasattr(session, 'email')
    )

@app.route('/items/add/')
def addItemForm():
    categories = dbSession.query(Item).distinct(Item.category).group_by(Item.category)
    return render_template('itemForm.html',
        categories=categories
    )

@app.route('/items/', methods=['POST'])
def addItem():
    newItem = Item(
        name = request.form['name'],
        description = request.form['description'],
        category = request.form['category'],
        createdBy = 1
    )
    dbSession.add(newItem)
    dbSession.commit()
    return redirect(url_for('homePage'))

@app.route('/items/<int:itemID>/edit/')
def editItemForm(itemID):
    item = dbSession.query(Item).filter_by(id=itemID).one()
    categories = dbSession.query(Item).distinct(Item.category).group_by(Item.category)
    return render_template('itemForm.html',
        item=item,
        categories=categories
    )

@app.route('/items/<int:itemID>/', methods=['PUT'])
def editItem(itemID):
    updatedItem = dbSession.query(Item).filter_by(id=itemID).one()
    updatedItem.name = request.form['name']
    updatedItem.description = request.form['description']
    updatedItem.category = request.form['category']

    dbSession.add(updatedItem)
    dbSession.commit()
    return redirect(url_for('homePage'))

@app.route('/items/<int:itemID>/delete/')
def deleteItemForm(itemID):
    item = dbSession.query(Item).filter_by(id=itemID).one()
    return render_template('itemDeleteForm.html',
        item=item
    )

@app.route('/items/<int:itemID>/', methods=['DELETE'])
def deleteItem(itemID):
    item = dbSession.query(Item).filter_by(id=itemID).one()
    dbSession.delete(item)
    dbSession.commit()
    return redirect(url_for('homePage'))

@app.route('/catalog/api/')
def getAllItems():
    items = dbSession.query(Item).all()
    return jsonify(items=[c.serialize for c in items])

app.debug = True
app.run(host='0.0.0.0', port=5000)
