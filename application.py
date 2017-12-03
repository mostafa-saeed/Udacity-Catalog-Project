import httplib2

from flask import (
    Flask, render_template, request,
    redirect, jsonify, url_for, session, make_response
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CONNECTION_STRING
from models.user import User
from models.item import Item
from functions import *

engine = create_engine(CONNECTION_STRING)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbSession = DBSession()

app = Flask(__name__)
app.secret_key = 'MY_APP_SECRET_KEY'

with app.open_resource('client_secrets.json') as f:
    GOOGLE_CLIENT_ID = json.load(f)['web']['client_id']


# CSRF check
# link: http://flask.pocoo.org/snippets/3/
@app.before_request
def csrf_protect():
    if '/items' in request.url and request.method in ['POST', 'PUT', 'DELETE']:
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            return unauthorizedResponse('Missing CSRF Token!')

app.jinja_env.globals['csrf_token'] = generate_csrf_token


# Home page route
@app.route('/')
def homePage():
    # Generate anti-forgery state token
    session['state'] = generateRandomToken()

    categories = getCategories()
    items = dbSession.query(Item).order_by(Item.id.desc()).limit(10)
    return render_template('home.html', categories=categories, items=items)


# Single category route
@app.route('/category/<string:categoryName>/')
@app.route('/category/<string:categoryName>/items/')
def getCategory(categoryName):
    items = dbSession.query(Item).filter_by(category=categoryName).all()
    return render_template(
                            'category.html',
                            categoryName=categoryName, items=items)


# Single item route
@app.route('/items/<int:itemID>/')
def getItem(itemID):
    item = dbSession.query(Item).filter_by(id=itemID).one()
    return render_template('item.html', item=item)


# Add item form
@app.route('/items/add/')
@login_required
def addItemForm():
    categories = getCategories()
    return render_template('addItemForm.html', categories=categories)


# Add item
@app.route('/items/', methods=['POST'])
@login_required
def addItem():
    ''' `Only for logged in users`
        When the user submits the form,
        The browser send a POST request containing the item data
        It collects these data and create new item in the database
        Then redirects the user to the home page
    '''
    newItem = Item(
        name=request.form['name'],
        description=request.form['description'],
        category=request.form['category'],
        createdBy=session['user_id']
    )
    dbSession.add(newItem)
    dbSession.commit()
    return redirect(url_for('homePage'))


# Edit item form
@app.route('/items/<int:itemID>/edit/')
@login_required
def editItemForm(itemID):
    # find the item with id of itemID variable
    item = dbSession.query(Item).filter_by(id=itemID).one()
    categories = getCategories()
    return render_template(
                            'editItemForm.html',
                            item=item, categories=categories)


# Edit item
@app.route('/items/<int:itemID>/', methods=['PUT'])
@login_required
def editItem(itemID):
    ''' Only for logged in users
        When the user submits the form,
        The browser send an AJAX PUT request containing the new item data
        It collects these data and update the item item in database
        Then redirects the user to the home page
    '''

    # find the item
    updatedItem = dbSession.query(Item).filter_by(id=itemID).one()

    # make sure that the item belongs to the logged in user
    if session['user_id'] != updatedItem.createdBy:
        return unauthorizedResponse('Wrong Access!')

    # update the item with the new data
    updatedItem.name = request.form['name']
    updatedItem.description = request.form['description']
    updatedItem.category = request.form['category']
    dbSession.add(updatedItem)
    dbSession.commit()
    return successResponse('Successfully Updated Item.')


# Delete item form
@app.route('/items/<int:itemID>/delete/')
@login_required
def deleteItemForm(itemID):
    item = dbSession.query(Item).filter_by(id=itemID).one()
    return render_template('deleteItemForm.html', item=item)


# Edit item
@app.route('/items/<int:itemID>/', methods=['DELETE'])
@login_required
def deleteItem(itemID):
    ''' Only for logged in users
        When the user submits the form, The browser send an AJAX DELETE request
        It delete that item from database
        Then redirects the user to the home page
    '''
    item = dbSession.query(Item).filter_by(id=itemID).one()

    # make sure that the item belongs to the logged in user
    if session['user_id'] != item.createdBy:
        return unauthorizedResponse('Wrong Access!')

    dbSession.delete(item)
    dbSession.commit()
    return successResponse('Successfully Deleted Item.')


# JSON API end point shows all items with their informaton
@app.route('/catalog/api/')
def getAllItems():
    items = dbSession.query(Item).all()
    return jsonify(items=[i.serialize for i in items])


# Login with GMail account
@app.route('/gconnect', methods=['POST'])
def gPlusLogin():

    if request.args.get('state') != session['state']:
        return unauthorizedResponse('Invalid state parameter')

    id_token = request.data

    # Use the token to get user's information from google
    url = (
        'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + id_token
    )
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # Verify that the id token is valid for this app
    if result['aud'] != GOOGLE_CLIENT_ID:
        response = unauthorizedResponse(
            "Token's client ID does not match app's")
        return response

    # Find or create new user
    user = getOrCreateUser(result['email'])

    # Get user info and store in login session
    session['email'] = result['email']
    session['user_id'] = user.id
    return successResponse('Successfully connected user.')


# Disconnect Google user
@app.route('/gdisconnect', methods=['POST'])
@login_required
def gPlusLogout():
    del session['email']
    del session['user_id']
    return successResponse('Successfully disconnected user.')

if __name__ == "__main__":
    app.debug = True
    app.run()
