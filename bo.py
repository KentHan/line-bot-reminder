# -*- coding: utf-8 -*-

from time import time

import sys
reload(sys)     
sys.setdefaultencoding("utf-8")

from dao import EventDAO
from event import Event
from message import send_text_message

class EventBO:
	dao = EventDAO()

	def handle_add_command(self, user, options):
		print(options)
		kv = dict(options)
		event = Event(kv["-n"], int(time()), int(kv["-t"]))
		if self.dao.has_user(user):
			return self.dao.append_event(user, event)
		else:
			return self.dao.add_user_and_event(user, event)

	def handle_remove_command(self, user, options):
		print("options: ", options)
		kv = dict(options)
		event = Event(kv["-n"])
		return self.dao.remove_event(user, event)

	def handle_reset_command(self, user, options):
		print("options: ", options)
		kv = dict(options)
		event = Event(kv["-n"])
		return self.dao.reset_event(user, event)

	def send_notification(self):
		users = self.dao.query_all_user_events()
		for user in users:
			user_id = user['_id']
			for event in user['events']:
				created_time = event['created_time']
				interval = event['interval']
				name = event['name']
				current_time = int(time())
				last_notified_time = event['last_notified_time'] if 'last_notified_time' in event else 0
				print("last_notified_time: ", last_notified_time)
				print("current_time:       ", current_time)
				if current_time - last_notified_time >= interval:
					times = (current_time - created_time) / int(interval)
					message = self.compose_alert_message(name, times, interval)
					send_text_message(user_id, message)
					self.dao.update_last_notified_time(user_id, name, current_time)

	def compose_alert_message(self, name, times, interval):
		times_string = "%d%s" % (times, "天" if interval==86400 else "次")
		output = "離上一次%s已經%s了！" % (name, times_string)
		return output