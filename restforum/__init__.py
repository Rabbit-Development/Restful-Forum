from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager

controller = Flask(__name__)
controller.config.from_pyfile('config.cfg')
db = MongoEngine(controller)
login_manager = LoginManager()
login_manager.init_app(controller)

from restforum import api

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

if __name__ == '__main__':
	controller.run()
