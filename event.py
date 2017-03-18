# -*- coding: utf-8 -*-

from time import time

class Event:
	
	def __init__(self, target, name, created_time=0, interval=0):
		self.target = target
		self.name = name
		self.created_time = created_time
		self.interval = interval

	def debug_print(self):
		print("name: %s" % self.name, 
			 	"created_time: %d" % self.created_time, 
			  	"interval: %d" % self.interval,
				"last_notified_time: %d" % self.last_notified_time)
				"current_time: %d" % int(time()))