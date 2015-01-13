from flask import Flask
from flask.ext.mongoengine import MongoEngine

controller = Flask(__name__)
controller.config.from_pyfile('config.cfg')
db = MongoEngine(controller)

if __name__ == '__main__':
	controller.run()
