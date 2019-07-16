# -*- coding: utf-8 -*-

import os

from pymongo import MongoClient

from util import Util

mongodb_id = os.getenv("MONGODB_ID")
mongodb_pw = os.getenv("MONGODB_PW")
mongodb_uri = os.getenv("MONGODB_URI")


class EventDAO:
    def __init__(self, client=None):
        if client is None:
            self.client = MongoClient(mongodb_uri)
            self.client.admin.authenticate(mongodb_id, mongodb_pw, mechanism='SCRAM-SHA-1')
        else:
            self.client = client
        self.db = self.client.user_data

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
        return list(cursor)

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
        cursor = self.db.event.find(
            {
                "target": event.target,
                "name": event.name
            }
        )
        return len(list(cursor)) == 1

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
        assigned_time = Util.parse_local_time_to_timestamp(event['alarm_time'])
        result = self.db.event.update_one(
            {
                "target": event["target"],
                "name": event["name"]
            },
            {
                "$set": {
                    'last_notified_time': assigned_time,
                    'created_time': assigned_time
                }
            }
        )
        return result.acknowledged

    def query_events_by_target(self, target):
        cursor = self.db.event.find(
            {
                "target": target
            })
        return list(cursor)

    def query_event_by_target_and_name(self, target, name):
        cursor = self.db.event.find(
            {
                "target": target,
                "name": name
            })
        return list(cursor)[0]
