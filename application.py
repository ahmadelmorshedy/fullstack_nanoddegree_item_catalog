#imports
from flask import Flask

app = Flask(__name__)

#Routes Examples (from https://docs.google.com/document/d/1jFjlq_f-hJoAZP8dYuo5H3xY62kGyziQmiv9EPIA7tM/pub?embedded=true)
#site/catalog/SnnowBoarding/items
#site/catalog/SnnowBoarding/SnowBoard
#site/catalog/SnowBoard/edit (SnowBoard is the item name)
#site/catalog/SnowBoard/delete (SnowBoard is the item name)

@app.route('/')
def categoriesIndex():
	return "Categories Index..."

@app.route('/catalog.json')
def categoriesIndexJSON():
	return "Categories Index JSON..."

@app.route('/catalog/<category_name>/items')
def categoryShow(category_name):
	return "%s category Show page - listing category items" % category_name

@app.route('/catalog/<category_name>/newItem', methods=['GET', 'POST'])
def newItem(category_name):
	return "Creating new Item for category %s" % category_name

@app.route('/catalog/<category_name>/<item_name>')
def itemsShow(category_name, item_name):
	return "Showing item %s in Category %s" % (item_name, category_name)

@app.route('/catalog/<item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
	return "Editing item %s" % item_name

@app.route('/catalog/<item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
	return "Deleting item %s" % item_name

@app.route('/login')
def login():
	return "Logging In..."

@app.route('/logout')
def logout():
	return "Logging out..."



if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)