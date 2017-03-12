# -*- coding: utf-8 -*-


class Event:
	
	def __init__(self, name, created_time=0, interval=0):
		self.name = name
		self.created_time = created_time
		self.interval = interval
	