# -*- coding: utf-8 -*-


from dao import EventDAO


class EventBO:
	dao = EventDAO()

	def handle_add_command(self, user, options):
		print("hello~")