from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from user import User
from main import Main

class Item(Main):
    __tablename__ = 'items'
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    createdBy = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

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

