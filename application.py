from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from classes.user import User
from classes.item import Item

from database_setup import Base, CONNECTION_STRING

engine = create_engine(CONNECTION_STRING)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

testItem = Item(name='Test',
                description='testing',
                category='CatalogItem',
                createdBy=1
                )
session.add(testItem)
session.commit()


from flask import Flask



app = Flask(__name__)
@app.route('/items/')
def getAllItems():
    items = session.query(Item).all()
    return items








app.debug = True
app.run(host='0.0.0.0', port=5000)

#=======================================================================