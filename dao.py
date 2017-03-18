# -*- coding: utf-8 -*-


import os
from time import time

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
		result = self.db.event.insert_one(
    		{
        		"target": user,
        		"name": event.name,
        		"created_time": event.created_time,
        		"interval": event.interval
    		}
		)
		return result.acknowledged

	def query_all_events(self):
		cursor = self.db.event.find()
		results = cursor[:]
		return results

	def update_last_notified_time(self, user, name, last_notified_time):
		result = self.db.event.update_one(
			{
				"target": user,
				"name": name
			},
			{
				"$set": {
					'last_notified_time': last_notified_time
				}
			}
		)
		return result.acknowledged

	def has_event(self, event):
		result = self.db.event.find(
			{
				"target": event.target,
				"name": event.name
			}
		)
		return result.count() == 1

	def add_event(self, event):
		result = self.db.event.insert_one(
			{
				"target": event.target,
				"name": event.name,
				"created_time": event.created_time,
        		"interval": event.interval
			}
		)
		return result.acknowledged

	def remove_event(self, event):
		result = self.db.event.delete_one(
			{
				"target": event.target,
				"name": event.name
			}
		)
		return result.acknowledged

	def reset_event(self, event):
		result = self.db.event.update_one(
			{
				"target": event.user,
				"name": event.name
			},
			{
				"$set": {
					'last_notified_time': 0,
					'created_time': int(time())
				}
			}
		)
		return result.acknowledged

	def query_events_by_target(self, target):
		cursor = self.db.event.find(
			{
				"target": target
			})
		events = cursor[:]
		return events

		