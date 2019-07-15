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
        one_minute, one_hour, one_day = 60, 3600, 86400
        if interval < one_hour:
            counter = "分鐘"
            scale = one_minute
        elif interval < one_day:
            counter = "小時"
            scale = one_hour
        else:
            counter = "天"
            scale = one_day

        times = time_diff_in_second / scale
        times = 0 if times < 0 else times
        return times, counter

    @staticmethod
    def parse_timestamp_to_local_time(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')