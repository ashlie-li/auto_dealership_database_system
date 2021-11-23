# Phase 3

## How to get started
1. use python 3

2. install mysql database client and start mysql database client
```sh
# For mac user
brew services install mysql
brew services start mysql
brew services stop mysql
```

3. create and activate virtual environment (optional)
```sh
# In order to separate depenecies and able to run flask command
# https://flask.palletsprojects.com/en/2.0.x/installation/

# create virtual environment
$ python3 -m venv venv

# activate virtual environment
. venv/bin/activate
```

4. install python dependencies
```sh
# install python library dependencies
pip3 install -r requirements.txt
```

5. Create database Load database schema
Note: (This only need to run once or rerun if you drop your database)
```sh
# log in database as root user
mysql -u root -p

# create database in sql console
CREATE DATABASE CS6400_try1;
exit;

# duplicate .env.sample to .env to override necessary database user password or user name

# load schema.sql and seed data
mysql -u root -p cs6400_try1 < app/schema.sql
```

6. Run flask app
```sh
python3 run.py
```
