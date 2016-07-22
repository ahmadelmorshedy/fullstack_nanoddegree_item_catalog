#imports
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from sqlalchemy import desc

# login imports
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets 
	# creates a flow object from the client secrets
	# json file, this json file stores your client ID,
	# client secret, and other oauth2 parameters

from oauth2client.client import FlowExchangeError

import httplib2 
# comprehensive http client librrary in Python 

import json 
# converts in memory python objects to a serialized representation (JSON)

from flask import make_response 
# converts the return value from a function into a real response object
# that we can send to our client

import requests 
# Apache 2 license HTTP library writeen in python, similar to urllib2 but with 
# few improvements

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///cameracatalogwithusers_6.db')
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
	if 'username' not in login_session:
		user = "guest"
	else:
		user = login_session['user_id']
	return render_template('categories.html', categories = categories, 
							last_items = last_items, user = user)

@app.route('/catalog.json')
def categoriesIndexJSON():
	categories = session.query(Category)
	return jsonify(Categories=[c.serialize for c in categories])

@app.route('/catalog/<category_name>/items')
def categoryShow(category_name):
	category = session.query(Category).filter_by(name = category_name).one()
	items = session.query(Item).filter_by(category_id = category.id)
	if 'username' not in login_session:
		user = "guest"
	else:
		user = login_session['user_id']
	return render_template('category_items.html', category = category, 
							items = items, user = user)

@app.route('/catalog/<category_name>/items.json')
def categoryShowJSON(category_name):
	category = session.query(Category).filter_by(name = category_name).one()
	items = session.query(Item).filter_by(category_id = category.id)
	return jsonify(CategoryItems=[i.serialize for i in items])

@app.route('/catalog/categories/new', methods=['GET', 'POST'])
def newCategory():
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		newCategory = Category(name = request.form['name'], user_id = login_session['user_id'])
		session.add(newCategory)
		session.commit()
		flash("New Category Created")
		return redirect(url_for('categoryShow', 
								category_name = request.form['name']))
	else:
		return render_template('new_category.html') 

@app.route('/catalog/<category_name>/edit', methods=['GET', 'POST'])
def editCategory(category_name):
	if 'username' not in login_session:
		return redirect('/login')
	category = session.query(Category).filter_by(name = category_name).one()
	if request.method == 'POST':
		session.query(Category).filter_by(id = category.id).update({"name": 
													request.form['name']})
		session.commit()
		flash("Category Edited Successfully")
		items = session.query(Item).filter_by(category_id = category.id)
		return redirect(url_for('categoryShow', 
									category_name = request.form['name']))
	else:
		return render_template('edit_category.html', category = category)

@app.route('/catalog/<category_name>/delete', methods=['GET', 'POST'])
def deleteCategory(category_name):
	if 'username' not in login_session:
		return redirect('/login')
	category = session.query(Category).filter_by(name = category_name).one()
	if request.method == 'POST':
		items = session.query(Item).filter_by(category_id = category.id)
		for item in items:
			session.delete(item)
		session.delete(category)
		session.commit()
		flash("Category Deleted")
		return redirect(url_for('categoriesIndex'))
	else:
		return render_template('delete_category.html', category = category)

@app.route('/catalog/<category_name>/items/new', methods=['GET', 'POST'])
def newItem(category_name):
	if 'username' not in login_session:
		return redirect('/login')
	category = session.query(Category).filter_by(name = category_name).one()
	if request.method == 'POST':
		newItem = Item(name = request.form['name'], 
						description  = request.form['description'], 
						category_id = category.id,
						user_id = login_session['user_id'])
		session.add(newItem)
		session.commit()
		flash("New Item Created")
		return redirect(url_for('itemShow', category_name = category_name, 
						item_name = request.form['name']))
	else:
		return render_template('new_item.html', category_name = category_name) 

@app.route('/catalog/<category_name>/<item_name>')
def itemShow(category_name, item_name):
	category = session.query(Category).filter_by(name = category_name).one()
	item = session.query(Item).filter_by(name = item_name).one()
	if 'username' not in login_session:
		user = "guest"
	else:
		user = login_session['user_id']
	return render_template('item.html', category = category, item = item, 
							user = user)
	#TODO >> Will I need Category there?

@app.route('/catalog/<item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
	if 'username' not in login_session:
		return redirect('/login')
	item = session.query(Item).filter_by(name = item_name).one()
	if request.method == 'POST':
		session.query(Item).filter_by(id = item.id).update(
						{"name": request.form['name'], 
						"description": request.form['description']})
		session.commit()
		flash("Item edited")
		return redirect(url_for('itemShow', category_name = item.category.name, 
						item_name = request.form['name']))
	else:
		return render_template('edit_item.html', item = item)

@app.route('/catalog/<item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
	if 'username' not in login_session:
		return redirect('/login')
	item = session.query(Item).filter_by(name = item_name).one()
	category = item.category
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		return redirect(url_for('categoryShow', category_name = category.name))
	else:
		return render_template('delete_item.html', item = item)

@app.route('/login')
def login():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)

@app.route('/logout')
def logout():
	return render_template('logout.html')

@app.route('/gconnect', methods=['POST'])
def gconnect():
	if request.args.get('state') != login_session['state']:
		flash("Login failed - Invalid State Parameter")
		return redirect(url_for('categoriesIndex'))
	code = request.data
	try:
		#upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		flash("Login failed - Failed to updgrade the authorization code")
		return redirect(url_for('categoriesIndex'))
	#check that the credentials object is valid
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % 
		access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	if result.get('error') is not None:
		flash("Login failed - error")
		return redirect(url_for('categoriesIndex'))
	#Verify that the access token is used for the intended user
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		flash("Login failed - Token's User ID desn't match given user id")
		return redirect(url_for('categoriesIndex'))
	#Verify that the access token is valid for this app
	if result['issued_to'] != CLIENT_ID:
		flash("Login failed - Token's Client ID desn't match app's.")
		return redirect(url_for('categoriesIndex'))
	#check to see if user is already signed in
	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		flash("Current User is already Connected.")
		return redirect(url_for('categoriesIndex'))

	#store the acces token in the session for later use
	login_session['credentials'] = credentials
	login_session['gplus_id'] = gplus_id

	#Get User Info
	userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
	params = {'access_token': credentials.access_token, 'alt':'json'}
	answer = requests.get(userinfo_url, params=params)
	data = json.loads(answer.text)

	login_session['provider'] = 'google'
	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	# See if user exists, if it dowsn't make a new one
	user_id = getUserId(login_session['email'])
	if user_id is None: #if not user_id (solution video)
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	flash("you are now logged in as %s" % login_session['username'])
	return redirect(url_for('categoriesIndex'))

#DISCONNECT
@app.route('/gdisconnect')
def gdisconnect():
	credentials = login_session.get('credentials')
	if credentials is None:
		response = make_response(json.dumps("Current User nort connected"), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	#Execute HTTP GET request to revoke current token
	access_token = credentials.access_token
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] == '200':
		#Reset user's session
		del login_session['credentials']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		del login_session['user_id']

		flash("You have successfully been logged out.")
		return redirect(url_for('categoriesIndex'))
	else:
		flash("Error During log out, please try again later.")
		return redirect(url_for('categoriesIndex'))

def getUserId(email):
	try:
		user = session.query(User).filter_by(email = email).one()
		return user.id
	except:
		return None

def getUserInfo(user_id):
	user = session.query(User).filter_by(id = user_id).one()
	return user

def createUser(login_session):
	newUser = User(name = login_session['username'], email = 
		login_session['email'], picture = login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email = login_session['email']).one()
	return user.id

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)