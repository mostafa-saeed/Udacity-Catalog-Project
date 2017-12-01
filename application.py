from flask import Flask, render_template, request, redirect, jsonify, url_for, session, make_response
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

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

#=======================================================================
def generateRandomToken():
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32)
    )

''' Get Categories from items table'''
def getCategories():
    itemsCategories = dbSession.query(Item).distinct(Item.category).group_by(Item.category, Item.id).all()
    categories = []
    for item in itemsCategories:
        categories.append(str(item.category))
    return categories

def unauthorizedResponse():
    response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response

GOOGLE_CLIENT_ID = '260872726788-7rlgebkleh2t57vut394puic1kbcf1jr.apps.googleusercontent.com'

#=======================================================================

app = Flask(__name__)
app.secret_key = generateRandomToken()

# isAuthenticated && isAuthorized
# responses
# Google+ Login

@app.route('/')
#@app.route('/catalog/')
def homePage():
    session['state'] = generateRandomToken()
    categories = getCategories()
    items = dbSession.query(Item).order_by(Item.id.desc()).limit(10)
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
    categories = getCategories()
    return render_template('addItemForm.html',
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
    categories = getCategories()
    return render_template('editItemForm.html',
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

@app.route('/gconnect/')
def gPlusLogin():
    if request.args.get('state') != session['state']:
        response = unauthorizedResponse()
        return response

    auth_code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(auth_code)
    except FlowExchangeError:
        return unauthorizedResponse()

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=' + access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    gplus_id = credentials.id_token['sub']

    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')

    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                200)
        response.headers['Content-Type'] = 'application/json'
        return response

    session['credentials'] = credentials
    session['gplus_id'] = gplus_id
    response = make_response(json.dumps('Successfully connected user.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response












if __name__ == "__main__":
    app.debug = True
    app.run()
