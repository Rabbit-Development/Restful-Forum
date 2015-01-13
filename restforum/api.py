from restforum import controller
from flask import request, abort, make_response, g
from flask.ext.login import login_user, login_required

@controller.route("/")
def hello():
	return "Hello there!"

@controller.route("/login", methods = ['POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return make_response("logged in")

	email = request.get('email')
	password = request.get('password')
	if any(email) and any(password) :
		user = User.objects(email=email)
		if user.verify_password(password):
			login_user(user)
			return make_response("logged in")
		else :
			abort(401)
	else:
		abort(400)

@controller.route("/register", methods = ['POST'])
def register():
	pass

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

@controller.route("/post", methods = ['POST'])
def post():
	return "posted"

@controller.route("/comment", methods = ['POST'])
def comment():
	pass

@controller.route("/topic", methods = ['POST'])
def topic():
	pass