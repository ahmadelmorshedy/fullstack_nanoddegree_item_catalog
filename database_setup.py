#Importing Section=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

#Create Classes=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class User(Base):
	__tablename__ = 'users'
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))
	id = Column(Integer, primary_key = True)

class Category(Base):
	__tablename__ = 'categories'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False, unique = True)
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return {
			'name': self.name,
			'id': self.id,
			'creator_email': self.user.email,
			'creator_id': self.user_id,
		}

class Item(Base):
	__tablename__ = 'items'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False, unique = True)
	description = Column(String(400), default = "No description available...")
	category_id = Column(Integer, ForeignKey('categories.id'))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return {
			'name': self.name,
			'id': self.id,
			'category_id': self.category_id,
			'category': self.category.name,
			'creator_email': self.user.email,
			'creator_id': self.user_id,
		}
#=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Configuration=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
engine = create_engine('sqlite:///cameracatalogwithusers_6.db')
Base.metadata.create_all(engine)