from sqlalchemy import create_engine

from models.main import Base

from models.user import User
from models.item import Item

DB_SERVER = 'localhost'
DB_USER = 'catalog'
DB_NAME = 'catalog'
DB_PASSWORD = '123'
CONNECTION_STRING = 'postgresql+psycopg2://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_SERVER + '/' + DB_NAME

engine = create_engine(CONNECTION_STRING)
Base.metadata.create_all(engine)
