#imports
from flask import Flask, render_template

app = Flask(__name__)

#Routes Examples (from https://docs.google.com/document/d/1jFjlq_f-hJoAZP8dYuo5H3xY62kGyziQmiv9EPIA7tM/pub?embedded=true)
#site/catalog/SnnowBoarding/items
#site/catalog/SnnowBoarding/SnowBoard
#site/catalog/SnowBoard/edit (SnowBoard is the item name)
#site/catalog/SnowBoard/delete (SnowBoard is the item name)

@app.route('/')
def categoriesIndex():
	return render_template('categories.html')

@app.route('/catalog.json')
def categoriesIndexJSON():
	return "Categories Index JSON..."

@app.route('/catalog/<category_name>/items')
def categoryShow(category_name):
	return render_template('category_items.html', category_name = category_name) 
	#TODO >> change category_name to category

@app.route('/catalog/<category_name>/newItem', methods=['GET', 'POST'])
def newItem(category_name):
	return render_template('new_item.html', category_name = category_name) 
	#TODO >> change category_name to category

@app.route('/catalog/<category_name>/<item_name>')
def itemsShow(category_name, item_name):
	return render_template('item.html', category_name = category_name, item_name = item_name)
	#TODO >> change category_name to category and item_name to item (Will I need Category there?)

@app.route('/catalog/<item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
	return render_template('edit_item.html', item_name = item_name)
	#TODO >> change item_name to item

@app.route('/catalog/<item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
	return render_template('delete_item.html', item_name = item_name)
	#TODO >> change item_name to item

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