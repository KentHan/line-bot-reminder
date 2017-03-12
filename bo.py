# -*- coding: utf-8 -*-

from time import time

from dao import EventDAO
from event import Event

class EventBO:
	dao = EventDAO()

	def handle_add_command(self, user, options):
		print(options)
		kv = dict(options)
		event = Event(kv["-n"], int(time()), int(kv["-t"]))
		return self.dao.add_event(user, event)