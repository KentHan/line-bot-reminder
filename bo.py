# -*- coding: utf-8 -*-


from dao import EventDAO
from event import Event

class EventBO:
	dao = EventDAO()

	def handle_add_command(self, user, options):
		print(options)

		event = Event("name1", 1489303274, 60)
		return self.dao.add_event(user, event)