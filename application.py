#imports
from flask import Flask,render_template,request,redirect,url_for,jsonify,flash

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

# setting app
app = Flask(__name__)

# loading client secrets
client_secrets_loaded = json.loads(open('client_secret.json', 'r').read())
CLIENT_ID = client_secrets_loaded['web']['client_id']

#creating DB engine session
engine = create_engine('sqlite:///cameracatalogwithusers_7.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# home page
@app.route('/')
def categoriesIndex():
	# read all categories from the DataBase
	categories = session.query(Category)
	# get last 10 items
	last_items = session.query(Item).order_by(desc(Item.id)).limit(10)
	# use setup_user_paramter to identify whether this is a user session or
	# guest session
	user = setup_user_parameter()
	return render_template('categories.html', categories = categories, 
							last_items = last_items, user = user)

# catalogs json API
@app.route('/categories.json')
def categoriesIndexJSON():
	# read all categories
	categories = session.query(Category)
	return jsonify(Categories=[c.serialize for c in categories])

# category show page
@app.route('/category/<category_name>/items')
def categoryShow(category_name):
	# find category by name
	category = session.query(Category).filter_by(name = category_name).one()
	# getting category items
	items = session.query(Item).filter_by(category_id = category.id)
	# checking user/guest session
	user = setup_user_parameter()
	return render_template('category_items.html', category = category, 
							items = items, user = user)

# category show JSON API
@app.route('/category/<category_name>/items.json')
def categoryShowJSON(category_name):
	category = session.query(Category).filter_by(name = category_name).one()
	items = session.query(Item).filter_by(category_id = category.id)
	return jsonify(CategoryItems=[i.serialize for i in items])

# create category
@app.route('/categories/new', methods=['GET', 'POST'])
def newCategory():
	if 'username' not in login_session:
		# redirect to login page
		return redirect('/login')
	if request.method == 'POST':
		# creating new category
		newCategory = Category(name = request.form['name'], 
									user_id = login_session['user_id'])
		session.add(newCategory)
		session.commit()
		flash("New Category Created")
		# redirect to newly created category show page
		return redirect(url_for('categoryShow', 
								category_name = request.form['name']))
	else:
		# rendering Category create form
		return render_template('new_category.html') 

# edit category
@app.route('/category/<category_name>/edit', methods=['GET', 'POST'])
def editCategory(category_name):
	if 'username' not in login_session:
		# redirect to login page
		return redirect('/login')
	print "Category name: %s" % category_name
	category = session.query(Category).filter_by(name = category_name).one()
	if request.method == 'POST':
		# updating category
		session.query(Category).filter_by(id = category.id).update({"name": 
													request.form['name']})
		session.commit()
		flash("Category Edited Successfully")
		# get possibly existing items
		items = session.query(Item).filter_by(category_id = category.id)
		# redirect to updated category show page
		return redirect(url_for('categoryShow', 
									category_name = request.form['name']))
	else:
		# rendering Category edit form
		return render_template('edit_category.html', category = category)

# delete category
@app.route('/category/<category_name>/delete', methods=['GET', 'POST'])
def deleteCategory(category_name):
	if 'username' not in login_session:
		# redirect to login page
		return redirect('/login')
	category = session.query(Category).filter_by(name = category_name).one()
	if request.method == 'POST':
		# deleting category
		items = session.query(Item).filter_by(category_id = category.id)
		for item in items:
			session.delete(item)
		session.delete(category)
		session.commit()
		flash("Category Deleted")
		# redirect to Home Page
		return redirect(url_for('categoriesIndex'))
	else:
		# rendering Category delete coonfirmation page
		return render_template('delete_category.html', category = category)

# create Item
@app.route('/category/<category_name>/items/new', methods=['GET', 'POST'])
def newItem(category_name):
	if 'username' not in login_session:
		# redirect to login page
		return redirect('/login')
	# load parent category
	category = session.query(Category).filter_by(name = category_name).one()
	if request.method == 'POST':
		# create item
		newItem = Item(name = request.form['name'], 
						description  = request.form['description'], 
						category_id = category.id,
						user_id = login_session['user_id'])
		session.add(newItem)
		session.commit()
		flash("New Item Created")
		# redirect to newly created Item Show page
		return redirect(url_for('itemShow', category_name = category_name, 
						item_name = request.form['name']))
	else:
		# rendering Item creation fform page
		return render_template('new_item.html', category_name = category_name) 

# Item Show
@app.route('/category/<category_name>/<item_name>')
def itemShow(category_name, item_name):
	# get item category
	category = session.query(Category).filter_by(name = category_name).one()
	# getiing Item
	item = session.query(Item).filter_by(name = item_name).one()
	# checking user/guest session
	user = setup_user_parameter()
	# render item show page
	return render_template('item.html', category = category, item = item, 
							user = user)
	#TODO >> Will I need Category there?

# edit Item
@app.route('/item/<item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
	if 'username' not in login_session:
		# redirect to login page
		return redirect('/login')
	# get Item
	item = session.query(Item).filter_by(name = item_name).one()
	if request.method == 'POST':
		# update Item
		session.query(Item).filter_by(id = item.id).update(
						{"name": request.form['name'], 
						"description": request.form['description']})
		session.commit()
		flash("Item edited")
		# redirect to Item show page
		return redirect(url_for('itemShow', category_name = item.category.name, 
						item_name = request.form['name']))
	else:
		# render Item edit form
		return render_template('edit_item.html', item = item)

# delete item
@app.route('/item/<item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
	if 'username' not in login_session:
		# redirect to login page
		return redirect('/login')
	# get item & category
	item = session.query(Item).filter_by(name = item_name).one()
	category = item.category
	if request.method == 'POST':
		# delete Item
		session.delete(item)
		session.commit()
		# return to item's category show page
		return redirect(url_for('categoryShow', category_name = category.name))
	else:
		# render Item deletion confirmation page
		return render_template('delete_item.html', item = item)

# login
@app.route('/login')
def login():
	# generate string
	generated_string = string.ascii_uppercase + string.digits
	print "login - string generated : {{generated_string}}"
	# use generated string to generate a random 32-length key
	state = ''.join(random.choice(generated_string) for x in xrange(32))
	print "login - state : {{state}}"
	login_session['state'] = state
	return render_template('login.html', STATE=state)

@app.route('/logout')
def logout():
	# return render_template('logout.html')
	return redirect(url_for('gdisconnect'))

@app.route('/gconnect', methods=['POST'])
def gconnect():
	# check for state variable
	print "gconnect - start"
	if request.args.get('state') != login_session['state']:
		print "gconnect Failure 1"
		flash("Login failed - Invalid State Parameter")
		return redirect(url_for('categoriesIndex'))
	code = request.data
	print "gconnect - got code"
	try:
		#upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
		print "gconnect - oauth_flow got"
		oauth_flow.redirect_uri = 'postmessage'
		print "gconnect - redirect_uri"
		credentials = oauth_flow.step2_exchange(code)
		print "gconnect - credentials set"
	except FlowExchangeError:
		print "gconnect - Failure 2"
		flash("Login failed - Failed to updgrade the authorization code")
		return redirect(url_for('categoriesIndex'))
	#check that the credentials object is valid
	access_token = credentials.access_token
	print "gconnect - access token set"
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % 
		access_token)
	h = httplib2.Http()
	print "gconnect - loading url"
	result = json.loads(h.request(url, 'GET')[1])
	if result.get('error') is not None:
		print "gconnect - Failure 3"
		flash("Login failed - error")
		return redirect(url_for('categoriesIndex'))
	#Verify that the access token is used for the intended user
	gplus_id = credentials.id_token['sub']
	print "gconnect - gplus_id set"
	if result['user_id'] != gplus_id:
		print "gconnect - Failure 4"
		flash("Login failed - Token's User ID desn't match given user id")
		return redirect(url_for('categoriesIndex'))
	#Verify that the access token is valid for this app
	if result['issued_to'] != CLIENT_ID:
		print "gconnect - Failure 5"
		flash("Login failed - Token's Client ID desn't match app's.")
		return redirect(url_for('categoriesIndex'))
	#check to see if user is already signed in
	print "gconnect - checking already signed in user"
	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		print "gconnect - Already Logged In"
		flash("Current User is already Connected.")
		print "gconnect - redirecting to categories Index"
		return redirect(url_for('categoriesIndex'))

	#store the acces token in the session for later use
	print "gconnect - saving user info & credentials"
	login_session['credentials'] = credentials
	login_session['gplus_id'] = gplus_id

	#Get User Info
	userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
	params = {'access_token': credentials.access_token, 'alt':'json'}
	answer = requests.get(userinfo_url, params=params)
	data = json.loads(answer.text)

	# store user info into login session
	login_session['provider'] = 'google'
	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	# See if user exists, if it dowsn't make a new one
	print "gconnect - checking new / existing User"
	user_id = getUserId(login_session['email'])
	if user_id is None: #if not user_id (solution video)
		print "gconnect - new User"
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	flash("you are now logged in as %s" % login_session['username'])
	# redirect to Home Page
	print "gconnect - Home Sweet Home"
	# return redirect(url_for('categoriesIndex'))
	response = make_response(json.dumps('Successfully logged in'), 200)
	response.headers['Content-Type'] = 'application/json'
	return response

#DISCONNECT
@app.route('/gdisconnect')
def gdisconnect():
	print "gdisconnect - start"
	credentials = login_session.get('credentials')
	if credentials is None:
		print "gdisconnect - Failure 1"
		response = make_response(json.dumps("Current User nort connected"), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	#Execute HTTP GET request to revoke current token
	access_token = credentials.access_token
	print "gdisconnect - got access token"
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	print "gdisconnect - calling ggooleapis"
	result = h.request(url, 'GET')[0]

	if result['status'] == '200':
		print "gdisconnect - resetting session"
		#Reset user's session
		del login_session['credentials']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		del login_session['user_id']

		flash("You have successfully been logged out.")
		print "gdisconnect - Home Sweet Home"
		return redirect(url_for('categoriesIndex'))
	else:
		print "gdisconnect - Failure 2"
		flash("Error During log out, please try again later.")
		return redirect(url_for('categoriesIndex'))

# method to search/get user Id by email
def getUserId(email):
	try:
		user = session.query(User).filter_by(email = email).one()
		return user.id
	except:
		return None

# method to get user info by Id
def getUserInfo(user_id):
	user = session.query(User).filter_by(id = user_id).one()
	return user

# registers a new User
def createUser(login_session):
	newUser = User(name = login_session['username'], email = 
		login_session['email'], picture = login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email = login_session['email']).one()
	return user.id

# checks whether there exists a loggged in user or not, returns either user id
# or "guest"
def setup_user_parameter():
	if 'username' not in login_session:
		return "guest" # guest
	return login_session['user_id'] # user logged in


# app setup
if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)