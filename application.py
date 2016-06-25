#imports
from flask import Flask, render_template, request

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

from sqlalchemy import desc

engine = create_engine('sqlite:///cameracatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#Routes Examples (from https://docs.google.com/document/d/1jFjlq_f-hJoAZP8dYuo5H3xY62kGyziQmiv9EPIA7tM/pub?embedded=true)
#site/catalog/SnnowBoarding/items
#site/catalog/SnnowBoarding/SnowBoard
#site/catalog/SnowBoard/edit (SnowBoard is the item name)
#site/catalog/SnowBoard/delete (SnowBoard is the item name)

@app.route('/')
def categoriesIndex():
	categories = session.query(Category)
	last_items = session.query(Item).order_by(desc(Item.id)).limit(10) #get last ten items
	return render_template('categories.html', categories = categories, last_items = last_items)

@app.route('/catalog.json')
def categoriesIndexJSON():
	return "Categories Index JSON..."

@app.route('/catalog/<category_name>/items')
def categoryShow(category_name):
	category = session.query(Category).filter_by(name = category_name).one()
	items = session.query(Item).filter_by(category_id = category.id)
	return render_template('category_items.html', category = category, items = items) 
	
@app.route('/catalog/<category_name>/items/new', methods=['GET', 'POST'])
def newItem(category_name):
	category = session.query(Category).filter_by(name = category_name).one()
	if request.method == 'POST':
		newItem = Item(name = request.form['name'], description  = request.form['description'], 
						category_id = category.id)
		session.add(newItem)
		session.commit()
		item = session.query(Item).filter_by(name = request.form['name']).one()
		return render_template('item.html', category = category, item = item)
	else:
		return render_template('new_item.html', category_name = category_name) 

@app.route('/catalog/<category_name>/<item_name>')
def itemShow(category_name, item_name):
	category = session.query(Category).filter_by(name = category_name).one()
	item = session.query(Item).filter_by(name = item_name).one()
	return render_template('item.html', category = category, item = item)
	#TODO >> Will I need Category there?

@app.route('/catalog/<item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
	item = session.query(Item).filter_by(name = item_name).one()
	if request.method == 'POST':
		session.query(Item).filter_by(id = item.id).update({"name": request.form['name'], 
						"description": request.form['description']})
		session.commit()
		category = session.query(Category).filter_by(id = item.category_id).one()
		return render_template('item.html', category = category, item = item)
	else:
		return render_template('edit_item.html', item = item)

@app.route('/catalog/<item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
	item = session.query(Item).filter_by(name = item_name).one()
	category = item.category
	if request.method == 'POST':
		session.delete(item)
		session.commit()

		items = session.query(Item).filter_by(category_id = category.id)
		return render_template('category_items.html', category = category, items = items)
	else:
		return render_template('delete_item.html', item = item)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	return render_template('logout.html')



if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)