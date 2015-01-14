from restforum.api import *
from flask import Response
from werkzeug.datastructures import Headers
from flask.ext.mongoengine import MongoEngine
import unittest, json

class TestAPI(unittest.TestCase):

	def user_tests(self):
		"""API: Testing User Handling"""
		#Register user
		self.controller = controller.test_client()
		self.controller.config["MONGODB_SETTINGS"] = {'DB' : 'test'}
		db = MongoEngine(self.controller)
		db.drop_database('test')
		expected = Response()
		expected.status_code = 200
		
		user_info = {
			'email':'user@test.com',
			'password':'password1!@',
			'username':'nick'
			}
		h = Headers()
		h.add('content-type', 'application/json')
		response = self.controller.post(
			path="/register",
			headers = h,
			data=json.dumps(user_info)
			)
		self.assertEquals(response.status, expected.status)

		#Loggin in user
		expected.status_code = 200
		user_info = {
			'email':'user@test.com',
			'password':'password1!@',
			}

		h = Headers()
		h.add('content-type', 'application/json')
		response = self.controller.post(
			path="/login",
			headers = h,
			data=json.dumps(user_info)
			)
		self.assertEquals(response.status, expected.status)

		#Log out user
		expected.status_code = 200
		response = self.controller.get(
			path="/logout"
			)
		self.assertEquals(response.status_code, expected.status)