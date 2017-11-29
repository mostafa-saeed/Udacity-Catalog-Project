from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from classes.user import User

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    createdBy = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, backref = 'users')

    @property
    def serialize(self):
        '''Return object data in JSON format'''
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'createdBy': self.createdBy
        }

