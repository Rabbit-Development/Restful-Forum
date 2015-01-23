from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
import os

controller = Flask(__name__)
controller.config.from_pyfile('config.cfg')
db = MongoEngine(controller)
login_manager = LoginManager()
login_manager.init_app(controller)

from restforum.models import User
from restforum import api

controller.config['SECRET_KEY'] = os.urandom(128)

@login_manager.user_loader
def load_user(userid):
    return User.objects.filter(id=userid).first()

if __name__ == '__main__':
	controller.run()
