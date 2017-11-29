import sys, os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

DB_SERVER = 'localhost'
DB_USER = 'catalog'
DB_NAME = 'catalog'
DB_PASSWORD = '123'
CONNECTION_STRING = 'postgresql+psycopg2://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_SERVER + '/' + DB_NAME

engine = create_engine(CONNECTION_STRING)
Base.metadata.create_all(engine)
