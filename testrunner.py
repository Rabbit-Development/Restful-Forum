import os
from restforum import controller
from restforum.models import *
from flask.ext.mongoengine import MongoEngine
from mongoengine import connect
import unittest, json, datetime

class controllerTestCase(unittest.TestCase):


	
	def setUp(self):
		controller.config['MONGODB_SETTINGS'] = {
			'db':'test_db',
		}
		User.objects.delete()
		Topic.objects.delete()
		
		db = MongoEngine(controller)
		self.controller = controller.test_client()

	def tearDown(self):
		db = connect('test_db')
		db.drop_database('test_db')

	def test_index(self):
		rv = self.controller.get('/')
		assert 200 == rv.status_code
		assert "Hello there!" in rv.data.decode('utf-8')

	def test_user_mng(self):
		"""API: Testing User Handling"""
		user_info = {
			'email':'useasdr@test.com',
			'password':'password1!@',
			'username':'nick'
			}

		# Registering user
		rv = self.controller.post('/register', data=json.dumps(user_info), headers={'content-type':'application/json'})
		assert "User registered" in rv.data.decode('utf-8')
		assert 200 == rv.status_code

	def test_post(self):

		post_info = {

			'body' :'Kveldens første test',
			'title' : 'Kveldens første title',
			'author' : "Alf Magnus skrev dette"

		}

		d = json.dumps(post_info)

		

		rv = self.controller.post('/post', data=d, headers={'content-type':'application/json'})

		assert "Post finished" in rv.data.decode('utf-8')
		assert 200 == rv.status_code




if __name__ == '__main__':
	unittest.main()