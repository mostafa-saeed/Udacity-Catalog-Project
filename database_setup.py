import sys, os
from sqlalchemy import create_engine

sys.path.append(os.path.join(os.path.dirname(__file__), 'class'))
from main import Base

DB_SERVER = 'localhost'
DB_USER = 'catalog'
DB_NAME = 'catalog'
DB_PASSWORD = ''
CONNECTION_STRING = 'postgresql+psycopg2://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_SERVER + '/' + DB_NAME

engine = create_engine(CONNECTION_STRING)
Base.metadata.create_all(engine)
