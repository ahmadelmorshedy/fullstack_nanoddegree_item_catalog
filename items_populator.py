from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

engine = create_engine('sqlite:///cameracatalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#Delete
items = session.query(Item)
for item in items:
    session.delete(item)

categories = session.query(Category)
for category in categories:
    session.delete(category)

session.commit()


#Add Categories
cat1 = Category(name = "Nikon")
session.add(cat1)

cat2 = Category(name = "Canon")
session.add(cat2)

cat3 = Category(name = "Sony")
session.add(cat3)

#Add Items
d5200 = Item(name = "Nikon D5200", description="entry-level DSLR", category_id = 1)
session.add(d5200)
d5300 = Item(name = "Nikon D5300", description="entry-level DSLR", category_id = 1)
session.add(d5300)
d7200 = Item(name = "Nikon D7200", description="enthusiast DSLR", category_id = 1)
session.add(d7200)

eos450d = Item(name = "Canon EOS 450D", description="entry-level DSLR", category_id = 2)
session.add(eos450d)
eos650d = Item(name = "Canon EOS 650D", description="entry-level DSLR", category_id = 2)
session.add(eos650d)
eos700d = Item(name = "Canon EOS 700D", category_id = 2)
session.add(eos700d)

alpha58A = Item(name = "Sony Alpha 58 A", category_id = 3)
session.add(alpha58A)
alpha77II = Item(name = "Sony Alpha 77 II", description="Advanced Amateur Camera", category_id = 3)
session.add(alpha77II)

session.commit()