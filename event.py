# -*- coding: utf-8 -*-

from time import time


class Event:

    DEFAULT_ALARM_TIME = "21:00"

    def __init__(self, target, name, created_time=0, interval=0, alarm_time=DEFAULT_ALARM_TIME, last_notified_time=0):
        self.target = target
        self.name = name
        self.created_time = created_time
        self.interval = interval
        self.last_notified_time = last_notified_time
        self.alarm_time = alarm_time

    def __str__(self):
        return f"target: {self.target}\n" \
            f"name: {self.name}\n" \
            f"created_time: {self.created_time}\n" \
            f"interval: {self.interval}\n" \
            f"last_notified_time: {self.last_notified_time}\n" \
            f"alarm_time: {self.alarm_time}\n" \
            f"current_time: {int(time())}"
