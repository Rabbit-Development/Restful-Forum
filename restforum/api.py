from restforum import controller, login_manager as lm
from restforum.models import *
from flask import request, abort, make_response, g
from flask.ext.login import login_user, login_required, current_user, logout_user
from mongoengine.errors import ValidationError
import json, datetime


@controller.route("/")
def hello():
	print(make_response("Hello there!"))
	return make_response("Hello there!")

@controller.before_request
def before_request():
	g.user = current_user

@controller.route("/login", methods = ['POST'])
def login():
	email = request.json.get('email')
	password = request.json.get('password')
	if email != None and password != None:
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
			abort(401)
	else:
		print('Missing data...')
		abort(400)

@controller.route("/register", methods = ['POST'])
def register():
	print('Starting request for creating a new user...')
	email = request.json.get('email')
	password = request.json.get('password')
	username = request.json.get('username')
	if email == None or password == None or username == None:
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

@controller.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return make_response("logged out")

@controller.route("/topics", methods = ['GET'])
def topics():
	topics = []
	for topic in Topic.objects.all():
		topics.append(topic.to_json())
	if topic == []:
		abort(404)
	return make_response(json.dumps(topics))

@controller.route("/<topic_id>", methods = ['GET'])
def posts(topic_id):
	if topic_id is None:
		abort(400)
	posts = []
	topic = Topic.objects.filter(id == topic_id).first()
	for post in Post.objects.filter(topic == topic.get_id()).all():
		posts.append(post.to_json())
	if posts == []:
		abort(404)
	return make_response(json.dumps(posts))

@controller.route("/post/<id>", methods = ['GET'])
@login_required
def get_post(id):
	if id is None:
		return abort(400)
	try:
		post = Post.objects.filter(id=id).first()
	except ValidationError:
		abort(400)
	if post is None:
		abort(404)
	return make_response(post.to_json())

@controller.route("/post", methods = ['POST'])
@login_required
def post():
	created_at = datetime.datetime.now()
	title = request.json.get('title')
	body = request.json.get('body')
	image_path = request.json.get('image_path')
	comments = request.json.get('comments')
	topic_id = request.json.get('topic')
	author = g.user.get_id()

	if author is None or title is None:
		print('Missing required data!')
		print('Aborting request!')
		return abort(400)
	if topic_id is None:
		post = Post(created_at=created_at,title = title, body = body, image_path=image_path, comments=comments, author=author)
		post.save()
		return make_response(json.dumps({'post-id':post.get_id()}))
	try:
		topic = Topic.objects.filter(id=topic_id).first()
	except ValidationError:
		print('Not a valid ObjectId!')
		print('Aborting request!')
		abort(400)
	if topic is None:
		print('Topic could not be found!')
		abort(404)
	post = Post(created_at=created_at,title = title, body = body, image_path=image_path, comments=comments, author=author, topic=topic)
	post.save()
	print('Post accepted')
	print('Post submitted')
	return make_response(json.dumps({'topic-id':topic.get_id(), 'post-id':post.get_id()}))

@controller.route("/comment", methods = ['POST'])
def comment():
	created_at = datetime.datetime.now()
	post_id = request.json.get('post-id')
	body = request.json.get('body')
	author = g.user.get_id()
	if author is None or body is None or post_id is None:
		print('Missing required data!')
		print('Aborting request!')
		return abort(400)
	try:
		post = Post.objects.filter(id=post_id).first()
	except ValidationError:
		print('Not a valid ObjectId!')
		print('Aborting request!')
		abort(400)
	if post is None:
		print('Post could not be found!')
		abort(404)
	post.comments.append(Comment(created_at=created_at, body=body, author=author))
	post.save()
	return make_response(json.dumps({'post-id':post.get_id()}))

@controller.route("/topic", methods = ['POST'])
@login_required
def topic():
	print('===========================')
	print('New Create Topic request...')
	title = request.json.get('title')
	restricted = request.json.get('restricted')
	description = request.json.get('description')

	if title is None or restricted is None:
		print('Missing required data!')
		print('Aborting request!')
		abort(400)
	print('Got all data!')
	print('Checking for duplicates...')
	if Topic.objects.filter(title=title).first() is not None:
		print('Topic allready existing!')
		print('Aborting request')
		abort(400)
	print('No duplicates!')
	print('Creating Topic...')
	topic = Topic(title=title, restricted=restricted, description=description)
	topic.save()
	print('Topic created!')
	print('===========================')
	return make_response(json.dumps({'topic-id':topic.get_id()}))

