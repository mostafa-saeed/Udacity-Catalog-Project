from sqlalchemy import Column, ForeignKey, Integer, String
from models.main import Main

class User(Main):
    __tablename__ = 'users'
    email = Column(String, nullable=False)
