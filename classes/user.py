from sqlalchemy import Column, ForeignKey, Integer, String
from classes.main import Main

class User(Main):
    __tablename__ = 'users'
    email = Column(String, nullable=False)
