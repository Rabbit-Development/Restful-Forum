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
		self.user_info = {
				'email':'user@test.com',
				'password':'password1!@',
				'username':'nick'
				}

		self.post_info = {
			'body' :'Kveldens første test',
			'title' : 'Kveldens første title',
			'topic_title' : 'Topic1'
		}

	def tearDown(self):
		db = connect('test_db')
		db.drop_database('test_db')

	def register(self):
		return self.controller.post('/register', data=json.dumps(self.user_info), headers={'content-type':'application/json'})

	def login(self):
		return self.controller.post('/login', data=json.dumps(self.user_info), headers={'content-type':'application/json'})

	def post(self):
		return self.controller.post('/post', data=json.dumps(self.post_info), headers={'content-type':'application/json'})

	def test_a_user_mng(self):
		"""API: Testing User Handling"""
		# Registering user
		rv = self.controller.post('/register', data=json.dumps(self.user_info), headers={'content-type':'application/json'})
		assert "User registered" in rv.data.decode('utf-8')
		assert 200 == rv.status_code

	def test_b_index(self):
		"""API: Testing Index"""
		rv = self.controller.get('/')
		assert 200 == rv.status_code
		assert "Hello there!" in rv.data.decode('utf-8')

	def test_b_post(self):
		"""API: Testing Posting"""
		rv = self.register()
		assert 200 == rv.status_code
		rv = self.login()
		assert 200 == rv.status_code
		d = json.dumps(self.post_info)
		rv = self.controller.post('/post', data=d, headers={'content-type':'application/json'})
		assert 200 == rv.status_code

	def test_b_get_post(self):
		rv = self.register()
		assert 200 == rv.status_code
		rv = self.login()
		assert 200 == rv.status_code
		rv = self.post()
		assert 200 == rv.status_code
		rv = self.get('post')

	if __name__ == '__main__':
		unittest.main()