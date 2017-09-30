# -*- coding: utf-8 -*-

from time import time

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from dao import EventDAO
from event import Event
from message import MessageApi
from util import Util

SECONDS_A_DAY = 86400


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
            created_time = Util.parse_local_time_to_timestamp(options["alarm_time"])
        else:
            created_time = int(time())

        event = Event(user, options["name"], created_time, int(options["interval"]) * SECONDS_A_DAY, options['alarm_time'])
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

        if not 'alarm_time' in event:
            event['alarm_time'] = Event.DEFAULT_ALARM_TIME

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
            last_notified_time = event['last_notified_time'] \
                if 'last_notified_time' in event else created_time

            if current_time - last_notified_time >= interval:
                time_diff = current_time - created_time
                event_desc = self.compose_alert_message(name, time_diff, interval)
                self.message_api.send_reset_confirm_message(target_id, name, event_desc)
                self.dao.update_last_notified_time(target_id, name, last_notified_time + interval)

    def compose_alert_message(self, name, time_diff_in_second, interval):
        times, counter = Util.calculate_diff_interval(time_diff_in_second, interval)
        times_string = "%d%s" % (times, counter)
        output = "離上一次\"%s\"已經%s了！" % (name, times_string)
        return output

    def compose_event_list_message(self, events):
        output = ""
        current_time=int(time())
        for event in events:
            time_diff = current_time - event["created_time"]
            times, counter = Util.calculate_diff_interval(time_diff, event["interval"])
            line = "%s： %d %s前" % (event["name"], times, counter)
            output += line + "\n"
        return output
