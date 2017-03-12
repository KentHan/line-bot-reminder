# -*- coding: utf-8 -*-


import os

from pymongo import MongoClient

from event import Event

mongodb_id = os.getenv("MONGODB_ID")
mongodb_pw = os.getenv("MONGODB_PW")
mongodb_uri = os.getenv("MONGODB_URI")

class EventDAO:
	client = MongoClient(mongodb_uri)
	client.admin.authenticate(mongodb_id, mongodb_pw, mechanism='SCRAM-SHA-1')
	db = client.user_data

	def add_user_and_event(self, user, event):
		result = self.db.users.insert_one(
    		{
        		"_id": user,
        		"events": [
        			{	
        				"name": event.name,
        				"created_time": event.created_time,
        				"interval": event.interval
        			}
        		]
    		}
		)
		return result.acknowledged

	def query_all_user_events(self):
		cursor = self.db.users.find()
		results = cursor[:]
		return results

	def update_last_notified_time(self, user, name, last_notified_time):
		result = self.db.users.update(
			{
				"_id": user,
				"events.name": name
			},
			{
				"$set": {
					'events.$.last_notified_time': last_notified_time
				}
			}
		)
		return result.acknowledged

	def has_user(self, user):
		result = self.db.users.find(
			{
				"_id": user
			}
		)
		return result.count() is 1

	def append_event(self, user, event):
		result = self.db.users.update_one(
			{
				"_id": user,
			},
			{
				"$addToSet": {
					"events": {
						"name": event.name,
        				"created_time": event.created_time,
        				"interval": event.interval
					}
				}
			}
		)
		return result.acknowledged

	def remove_event(self, user, event):
		result = self.db.users.update_one(
			{
				"_id": user
			},
			{
				"$pull": {
					"events": {
						"name": event.name
					}
				}
			}
		)
		return result.acknowledged

	def query_event_from_user(self, user):
		pass

		