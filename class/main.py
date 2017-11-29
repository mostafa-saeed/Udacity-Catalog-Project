from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Main(Base):
    __tablename__ = ''
    id = Column(Integer, primary_key=True, autoincrement=True)

