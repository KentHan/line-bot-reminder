from datetime import datetime
from time import time, mktime


class Util(object):
    @staticmethod
    def parse_local_time_to_timestamp(inputted_hour_and_minute):
        today = datetime.fromtimestamp(int(time())).strftime('%Y-%m-%d')
        composed_datetime_string = "%s %s" % (today, inputted_hour_and_minute)

        assigned_timestamp = int(mktime(datetime.strptime(composed_datetime_string, "%Y-%m-%d %H:%M").timetuple()))
        return assigned_timestamp