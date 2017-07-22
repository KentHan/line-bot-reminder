# -*- coding: utf-8 -*-

from time import time, mktime
from datetime import datetime

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from dao import EventDAO
from event import Event
from message import MessageApi


class EventBO:
    def __init__(self, dao=None, message_api=None):
        if dao == None:
            dao = EventDAO()
        if message_api == None:
            message_api = MessageApi()

        self.dao = dao
        self.message_api = message_api

    def set_dao(self, dao):
        self.dao = dao

    def handle_add_command(self, user, options):
        print(options)

        if "alarm_time" in options:
            created_time = self.parse_local_time_to_timestamp(options["alarm_time"])
        else:
            created_time = int(time())

        event = Event(user, options["name"], created_time, int(options["interval"]))
        if self.dao.has_event(event):
            pass
        else:
            return self.dao.add_event(event)

    def handle_remove_command(self, user, options):
        print("options: ", options)
        event = Event(user, options["name"])
        return self.dao.remove_event(event)

    def handle_reset_command(self, user, options):
        print("options: ", options)
        event = self.dao.query_event_by_target_and_name(user, options["name"])
        return self.dao.reset_event(event)

    def handle_list_command(self, target_id, options=None):
        print("options:", options)
        events = self.dao.query_events_by_target(target_id)
        if len(events) > 0:
            self.message_api.send_text_message(target_id, self.compose_event_list_message(events))
        else:
            self.message_api.send_text_message(target_id, "No event!")

    def send_notification(self, current_time=int(time())):
        events = self.dao.query_all_events()
        for event in events:
            target_id = event['target']
            created_time = event['created_time']
            interval = event['interval']
            name = event['name']
            last_notified_time = event['last_notified_time'] if 'last_notified_time' in event and event[
                                                                                                      'last_notified_time'] != 0 else created_time

            if current_time - last_notified_time >= interval:
                time_diff = current_time - created_time
                message = self.compose_alert_message(name, time_diff, interval)
                self.message_api.send_text_message(target_id, message)
                self.message_api.send_reset_confirm_message(target_id, name)
                self.dao.update_last_notified_time(target_id, name, last_notified_time + interval)

    def compose_alert_message(self, name, time_diff, interval):
        if interval < 3600:
            counter = "分鐘"
            scale = 60
        elif interval < 86400:
            counter = "小時"
            scale = 3600
        else:
            counter = "天"
            scale = 86400

        times = time_diff / scale
        times_string = "%d%s" % (times, counter)
        output = "離上一次\"%s\"已經%s了！" % (name, times_string)
        return output

    def compose_event_list_message(self, events):
        output = ""
        for event in events:
            if "last_notified_time" in event and event["last_notified_time"] != 0:
                line = "%s: %d (%s)" % (event["name"], event["interval"],
                                        self.parse_timestamp_to_local_time(event["last_notified_time"]))
            else:
                line = "%s: %d" % (event["name"], event["interval"])
            output += line + "\n"
        return output

    def parse_local_time_to_timestamp(self, inputted_hour_and_minute):
        today = datetime.fromtimestamp(int(time())).strftime('%Y-%m-%d')
        composed_datetime_string = "%s %s" % (today, inputted_hour_and_minute)

        assigned_timestamp = int(mktime(datetime.strptime(composed_datetime_string, "%Y-%m-%d %H:%M").timetuple()))
        return assigned_timestamp

    def parse_timestamp_to_local_time(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
