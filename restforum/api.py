from restforum import controller, login_manager as lm
from restforum.models import *
from flask import request, abort, make_response, g
from flask.ext.login import login_user, login_required
import json, datetime


@controller.route("/")
def hello():
	print(make_response("Hello there!"))
	return make_response("Hello there!")

@controller.route("/login", methods = ['POST'])
def login():
	email = request.json.get('email')
	password = request.json.get('password')
	if any(email) and any(password):
		print('Have required data!')
		print('email:' + email)
		print('password' + password)
		print('Finds user...')
		user = User.objects.filter(email=email).first()
		if user is not None:
			print('Found user!')
			print('Verifies password...')
			if user.verify_password(password):
				print('Password verified!')
				print('Logging in user...')
				loggedin = login_user(user)
				print('User logged in!')
				return make_response("logged in")
			else :
				print('Wrong password aborting...')
				abort(401)
		else:
			print('Did not find user...')
			abort(404)
	else:
		print('Missing data...')
		abort(400)

@controller.route("/register", methods = ['POST'])
def register():
	print('Starting request for creating a new user...')
	email = request.json.get('email')
	password = request.json.get('password')
	username = request.json.get('username')
	if not any(email) or not any(password) or not any(username):
		print('Missing required data!')
		print('Aborting request!')
		return abort(400)
	else:
		print('Have required data!')
		print('email: ' + email)
		print('password: ' + password)
		print('Checking for duplicates...')
		if User.objects.filter(email=email).first() is None:
			print('No duplicates!')
			print('Creating new user...')
			user = User(email=email, username=username)
			pwd = user.hash_password(password)
			user.password = pwd
			user.save()
			print('User created!')
			return make_response("User registered")
		else: 
			print('Tried to create an allready existing user!')
			print('Aborting request!')
			return abort(400)

@controller.route("/logout")
@login_required
def logout():
    logout_user()
    return make_response("logged out")

@controller.route("/topics", methods = ['GET'])
def topics():
	return "topics"

@controller.route("/posts", methods = ['GET'])
def posts():
	return "posts"

@controller.route("/comments", methods = ['GET'])
def comments():

	pass

@login_required
@controller.route("/post", methods = ['POST'])
def post():
	created_at = datetime.datetime.now()
	title = request.json.get('title')
	body = request.json.get('body')
	image_path = request.json.get('image_path')
	comments = request.json.get('comments')
	author = g.user.get_id()

	if author is None or title is None:
		print('Missing required data!')
		print('Aborting request!')
		return abort(400)
	elif any(author) and any(title):
		print('Post accepted')
		post = Post(created_at=created_at,title = title, body = body, image_path=image_path, comments=comments, author=author)
		post.save()
		print('Post submitted')
		return make_response('Post finished') 
	else:
		print('Something went wrong')
		print('Aborting request')
		return abort(400)

@controller.route("/comment", methods = ['POST'])
def comment():

	
	pass

@controller.route("/topic", methods = ['POST'])
def topic():
	pass