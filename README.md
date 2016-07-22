# Item Catalog - Udacity project

This project is part of the [udacity fullstack nanodegree](https://www.udacity.com/degrees/full-stack-web-developer-nanodegree--nd004)


## Setup

1. clone project

2. follow this [link](https://www.udacity.com/course/viewer#!/c-nd004/l-3487760229/m-3631038670) to install vagrant to your machine 

3. copy the code from (1) to /vagrant folder set up after (2)

4. open a terminal, navigate to `vagrant` folder

5. execute `vagrant up` then `vagrant ssh`

6. once logged into the vagrant instance, type `cd /vagrant/catalog` to get into the project folder

7. execute following commands
	1. `python database_setup.py` to setup the database
	2. `python items_populator.py` to initiate some data in the database
	3. `python application.py` to run the application

8. open localhost:8000 in your browser