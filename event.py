# -*- coding: utf-8 -*-

from time import time


class Event:
    def __init__(self, target, name, created_time=0, interval=0, alarm_time="21:00", last_notified_time=0):
        self.target = target
        self.name = name
        self.created_time = created_time
        self.interval = interval
        self.last_notified_time = last_notified_time
        self.alarm_time = alarm_time

    def __str__(self):
        return "target: {}\nname: {}\ncreated_time: {}\ninterval: {}\nlast_notified_time: {}\n alarm_time: {}\ncurrent_time: {}".format(
            self.target,
            self.name,
            self.created_time,
            self.interval,
            self.last_notified_time,
            self.alarm_time,
            int(time()))
