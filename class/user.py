from sqlalchemy import Column, ForeignKey, Integer, String
import main

class User(main):
    __tablename__ = 'users'
    email = Column(String, nullable=False)
