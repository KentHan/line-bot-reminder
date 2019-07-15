# -*- coding: utf-8 -*-

from datetime import datetime
from time import time, mktime


class Util(object):
    @staticmethod
    def parse_local_time_to_timestamp(inputted_hour_and_minute):
        today = datetime.fromtimestamp(int(time())).strftime('%Y-%m-%d')
        composed_datetime_string = "%s %s" % (today, inputted_hour_and_minute)

        assigned_timestamp = int(mktime(datetime.strptime(composed_datetime_string, "%Y-%m-%d %H:%M").timetuple()))
        return assigned_timestamp

    @staticmethod
    def calculate_diff_interval(time_diff_in_second, interval):
        if interval < 3600:
            counter = "分鐘"
            scale = 60
        elif interval < 86400:
            counter = "小時"
            scale = 3600
        else:
            counter = "天"
            scale = 86400

        times = time_diff_in_second / scale
        times = 0 if times < 0 else times
        return times, counter

    @staticmethod
    def parse_timestamp_to_local_time(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')