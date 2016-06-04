#Importing Section=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

#Create Classes=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Category(Base):
	__tablename__ = 'categories'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False, unique = True)

class Item(Base):
	__tablename__ = 'items'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False, unique = True)
	description = Column(String(400), default = "No description available...")
	category_id = Column(Integer, ForeignKey('categories.id'))
	category = relationship(Category)
#=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Configuration=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
engine = create_engine('sqlite:///cameracatalog.db')
Base.metadata.create_all(engine)