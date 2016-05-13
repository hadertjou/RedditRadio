# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, json, session, redirect
from werkzeug import generate_password_hash, check_password_hash
import redditsearcher
import dbProc
from app import app, db, celery
#from flask.ext.mysql import MySQL
#from flask_sqlalchemy import SQLAlchemy
#from flask.ext.sqlalchemy import SQLAlchemy
#app = Flask(__name__)
#mysql = MySQL()
#uri = 'mysql://{username}:{password}@localhost/{dbname}'
#app.config['SQLALCHEMY_DATABASE_URI'] = uri
#db = SQLAlchemy(app)

#THIS FILE IS VIEWS.PY

@app.route("/")
def main():
	if session.get('user'):		
		return render_template('userHome.html')
	else:
		return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	return render_template('signUp.html')

@app.route('/signUp', methods=['POST'])
def signUp():
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']

	if _name and _email and _password:
		_hashed_password = generate_password_hash(_password)
		data = dbProc.addUser(_name, _email,_hashed_password)

		if data is 1:
			#conn.commit()
			return json.dumps({'message':'User created successfully !'})
		else:
			return json.dumps({'message': 'user already exists!'})#str(data[0])})
	else:
		return json.dumps({'message':'Please fill in all fields'})

	return ({'message':'wompwompwomp'})


@app.route('/showSignIn')
def showSignIn():
	return render_template('signIn.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():
	try:
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		data = dbProc.validateUser(_email)

		if data is not None:
		    if check_password_hash(data.password, _password):
		    	session['user'] = data.username
		        return redirect('/userHome')
		    else:
		        return render_template('error.html',error = 'Wrong Email address or Password.')
		else:
		    return render_template('error.html',error = 'Wrong Email address or Password.')

	except Exception as e:
		return render_template('error.html',error = str(e))

@app.route('/userHome')
def userHome():
	if session.get('user'):		
		return render_template('userHome.html')
	else:
		return render_template('error.html', error='Unauthorized access')

@app.route('/radio', methods=['POST'])
def radio():
	try:
		_subreddit = request.form['inputSub']
		_threadCount = request.form['inputQuantity']
		print "threadcount received: ", _threadCount
		if session.get('user') and _subreddit and _threadCount:
			person = session.get('user')
			redditsearcher.readPosts.delay(_subreddit, person, _threadCount)
			return json.dumps({'message':'Fetching!'})
		else:
			return json.dumps({'message':'Please fill in all fields, or User Authentication Error'})
		#if _subreddit is not None:
		#	redditsearcher.readPosts(_subreddit, person) #readPosts adds and commits all posts to db
		#else:
		#	return render_template('userHome.html', error='please enter valid subreddit')


	except Exception as e:
		return json.dumps({'message': str(e)})
		#return render_template('error.html', error = str(e))

@app.route('/getLine')
def getline():
	try:
		if session.get('user'):
			print "in getline"
			_user = session.get('user')
			pp = dbProc.getPerson(_user)
			print "pp queried"
			para = dbProc.getParagraph(pp)
			dbProc.deleteParagraph(para)

			return json.dumps({'paragraph': para.text})
			
		else:
			return render_template('error.html', error = 'Unauthorized access')
	except Exception as e:
		return json.dumps({'paragraph': '-1: FINISHED: -1'})
		#return render_template('error.html', error = str(e))


@app.route('/flush')
def flush():
	try:
		if session.get('user'):
			print "in flush"
			_user = session.get('user')
			pp = dbProc.getPerson(_user)
			dbProc.flushAll(pp)
			return json.dumps({'message': 'Finished Flushing!'})
		else:
			return render_template('error.html', error = 'Unauthorized access')

	except Exception as e:
		return render_template('error.html', error = str(e))


@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect('/')
	