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
			'body' :'Test Post',
			'title' : 'Test Post Title'
		}

		self.topic_info = {
			'title':'Test Topic',
			'restricted':False,
			'description':'Topic Test description'
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

	def get_post(self, rv):
		return self.controller.get('/post/' + json.loads(rv.data.decode('utf-8')).get('post-id'))

	def comment(self, post_id):
		d = json.dumps({'post-id':post_id, 'body': 'Test Comment'})
		return self.controller.post('/comment', data=d, headers={'content-type':'application/json'})

	def create_topic(self):
		return self.controller.post('/topic', data=json.dumps(self.topic_info), headers={'content-type':'application/json'})

	def test_user_mng(self):
		"""API: Testing User Handling"""
		# Registering user
		rv = self.controller.post('/register', data=json.dumps(self.user_info), headers={'content-type':'application/json'})
		assert "User registered" in rv.data.decode('utf-8')
		assert 200 == rv.status_code
		# Duplicate 
		rv = self.controller.post('/register', data=json.dumps({
			'email':'user@test.com',
			'password':'password1!@',
			'username':'nick'
		}), headers={'content-type':'application/json'})
		assert 400 == rv.status_code
		# Missing email
		rv = self.controller.post('/register', data=json.dumps({
			'password':'password1!@',
			'username':'nick'
		}), headers={'content-type':'application/json'})
		assert 400 == rv.status_code
		# Missing password
		rv = self.controller.post('/register', data=json.dumps({
			'email':'user@test.com',
			'username':'nick'
		}), headers={'content-type':'application/json'})
		assert 400 == rv.status_code
		# Missing username
		rv = self.controller.post('/register', data=json.dumps({
			'email':'user@test.com',
			'password':'password1!@',
		}), headers={'content-type':'application/json'})
		assert 400 == rv.status_code

	def test_login(self):
		"""API: Log in"""
		rv = self.register()
		assert 200 == rv.status_code
		# Correct input
		rv = self.controller.post('/login', data=json.dumps(self.user_info), headers={'content-type':'application/json'})
		assert 200 == rv.status_code
		# Missing email
		rv = self.controller.post('/login', data=json.dumps({
			'password':'password1!@',
		}), headers={'content-type':'application/json'})
		assert 400 == rv.status_code
		# Missing password
		rv = self.controller.post('/login', data=json.dumps({
			'email':'user@test.com',
		}), headers={'content-type':'application/json'})
		assert 400 == rv.status_code
		# Wrong email
		rv = self.controller.post('/login', data=json.dumps({
			'email':'wronguser@test.com',
			'password':'password1!@'
		}), headers={'content-type':'application/json'})
		assert 401 == rv.status_code
		# Wrong password
		rv = self.controller.post('/login', data=json.dumps({
			'email':'user@test.com',
			'password':'wrongpassword1!@'
		}), headers={'content-type':'application/json'})
		assert 401 == rv.status_code

	def test_logout(self):
		"""API: Log out"""
		rv = self.register()
		assert 200 == rv.status_code
		rv = self.login()
		assert 200 == rv.status_code
		rv = self.controller.get('/logout')
		assert 200 == rv.status_code

	def test_index(self):
		"""API: Testing Index"""
		rv = self.controller.get('/')
		assert 200 == rv.status_code
		assert "Hello there!" in rv.data.decode('utf-8')

	def test_post(self):
		"""API: Testing Posting"""
		rv = self.register()
		assert 200 == rv.status_code
		rv = self.login()
		assert 200 == rv.status_code
		# Correct input without topic
		rv = self.controller.post('/post', data=json.dumps(self.post_info), headers={'content-type':'application/json'})
		assert 200 == rv.status_code
		# Correct input with topic
		topic_id = json.loads(self.create_topic().data.decode('utf-8')).get('topic-id')
		rv = self.controller.post('/post', data=json.dumps({
			'body' :'Test Post',
			'title' : 'Test Post Title',
			'topic' : topic_id
			}), headers={'content-type':'application/json'})
		assert 200 == rv.status_code
		# Missing title
		rv = self.controller.post('/post', data=json.dumps({
			'body' :'Test Post',
			'topic' : topic_id
			}), headers={'content-type':'application/json'})
		assert 400 == rv.status_code
		# Wrong topic request
		rv = self.controller.post('/post', data=json.dumps({
			'body' :'Test Post',
			'title' : 'Test Post Title',
			'topic' : 'wrongtopic' 
			}), headers={'content-type':'application/json'})
		assert 400 == rv.status_code
		# Topic doesn't exist
		rv = self.controller.post('/post', data=json.dumps({
			'body' :'Test Post',
			'title' : 'Test Post Title',
			'topic' : '123456789012345678901234', #MongoDB uses 24byte hex as id keys
			}), headers={'content-type':'application/json'})
		assert 404 == rv.status_code

	def test_get_post(self):
		"""API: Testing Get Post"""
		rv = self.register()
		assert 200 == rv.status_code
		rv = self.login()
		assert 200 == rv.status_code
		rv = self.post()
		assert 200 == rv.status_code
		#Correct input
		post_id = json.loads(rv.data.decode('utf-8')).get('post-id')
		rv = self.controller.get('/post/' + post_id)
		assert 200 == rv.status_code
		#Missing input
		rv = self.controller.get('/post/')
		assert 404 == rv.status_code
		#Non existent post
		rv = self.controller.get('/post/123456789012345678901234')
		assert 404 == rv.status_code
		#Wrong input
		rv = self.controller.get('/post/wronginput')
		assert 400 == rv.status_code


	def test_comment(self):
		"""API: Testing Comment"""
		rv = self.register()
		assert 200 == rv.status_code
		rv = self.login()
		assert 200 == rv.status_code
		rv = self.post()
		assert 200 == rv.status_code
		post_id = json.loads(rv.data.decode('utf-8')).get('post-id')
		# Testing correct input
		d = json.dumps({'post-id':post_id, 'body': 'Test Comment'})
		rv = self.controller.post('/comment', data=d, headers={'content-type':'application/json'})
		assert 200 == rv.status_code
		rv = self.get_post(rv)
		assert json.loads(rv.data.decode('utf-8')).get('comments') != None
		# Missing post-id
		d = json.dumps({'body': 'Test Comment'})
		rv = self.controller.post('/comment', data=d, headers={'content-type':'application/json'})
		assert 400 == rv.status_code
		# Missing body
		d = json.dumps({'post-id':post_id})
		rv = self.controller.post('/comment', data=d, headers={'content-type':'application/json'})
		assert 400 == rv.status_code
		# Wrong post-id
		d = json.dumps({'post-id':'wrongpost', 'body': 'Test Comment'})
		rv = self.controller.post('/comment', data=d, headers={'content-type':'application/json'})
		assert 400 == rv.status_code
		# Non existent post
		d = json.dumps({'post-id':'123456789012345678901234', 'body': 'Test Comment'})
		rv = self.controller.post('/comment', data=d, headers={'content-type':'application/json'})
		assert 404 == rv.status_code

	def test_topic(self):
		"""API: Testing Creating Topic"""
		rv = self.register()
		assert 200 == rv.status_code
		rv = self.login()
		assert 200 == rv.status_code
		# Correct input
		d = json.dumps(self.topic_info)
		rv = self.controller.post('/topic', data=d, headers={'content-type':'application/json'})
		assert 200 == rv.status_code
		# Duplicate topic
		d = json.dumps(self.topic_info)
		rv = self.controller.post('/topic', data=d, headers={'content-type':'application/json'})
		assert 400 == rv.status_code
		# Missing title
		d = json.dumps({'restricted':False})
		rv = self.controller.post('/topic', data=d, headers={'content-type':'application/json'})
		assert 400 == rv.status_code
		# Missing restricted
		d = json.dumps({'title':'topic1'})
		rv = self.controller.post('/topic', data=d, headers={'content-type':'application/json'})
		assert 400 == rv.status_code

	def test_get_topics(self):
		"""API: Getting Topics"""
		rv = self.register()
		assert 200 == rv.status_code
		rv = self.login()
		assert 200 == rv.status_code
		rv = self.create_topic()
		assert 200 == rv.status_code
		rv = self.controller.get('/topics')
		assert 200 == rv.status_code
		assert json.loads(rv.data.decode('utf-8'))[0] != None

	def test_get_posts(self):
		"""API: Testing Getting Posts Given By Topic ID"""
		rv = self.register()
		assert 200 == rv.status_code
		rv = self.login()
		assert 200 == rv.status_code
		rv = self.create_topic()
		assert 200 == rv.status_code
		d = json.dumps({'body':'asd', 'title':'asdas', 'topic':json.loads(rv.data.decode('utf-8')).get('topic-id')})
		rv = self.controller.post('/post', data=d, headers={'content-type':'application/json'})
		assert 200 == rv.status_code
		topic_id = json.loads(rv.data.decode('utf-8')).get('topic-id')
		rv = self.controller.get('/' + topic_id)
		assert 200 == rv.status_code

	if __name__ == '__main__':
		unittest.main()