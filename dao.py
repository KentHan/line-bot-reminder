# -*- coding: utf-8 -*-


import os

from pymongo import MongoClient


mongodb_id = os.getenv("MONGODB_ID")
mongodb_pw = os.getenv("MONGODB_PW")
mongodb_uri = os.getenv("MONGODB_URI")

class EventDAO:
	client = MongoClient(mongodb_uri)
	client.admin.authenticate(mongodb_id, mongodb_pw, mechanism='SCRAM-SHA-1')
	db = client.user_data

	def add_event(self, event):
		pass

	def query_event_from_user(self):
		pass

	def query_event(self, user):
		pass

	def remove_event(self):
		pass