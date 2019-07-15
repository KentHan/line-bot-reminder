#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mock import patch

# from pymongo import MongoClient

from app import app
from app import command_parser
from bo import EventBO
from event import Event
from dao import EventDAO
from util import Util


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_page_works(self):
        rv = self.app.get('/')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)

    def test_about_page_works(self):
        rv = self.app.get('/about/')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)

    def test_404_page(self):
        rv = self.app.get('/i-am-not-found/')
        self.assertEqual(rv.status_code, 404)

    def test_static_text_file_request(self):
        rv = self.app.get('/robots.txt')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)
        rv.close()

    def test_input_add_parameters(self):
        input = "/add clean 86400 %s" % (Event.DEFAULT_ALARM_TIME)
        output_options = command_parser(input)
        self.assertEqual(output_options, {"name": "clean",
                                          "interval": "86400",
                                          "alarm_time": Event.DEFAULT_ALARM_TIME})

    def test_input_remove_parameters(self):
        input = "/remove clean"
        output_options = command_parser(input)
        self.assertEqual(output_options, {"name": "clean"})

    def test_input_reset_parameters(self):
        input = "/reset clean"
        output_options = command_parser(input)
        self.assertEqual(output_options, {"name": "clean"})

    def test_input_list_parameters(self):
        input = "/list"
        output_options = command_parser(input)
        self.assertEqual(output_options, {})

    @patch('dao.EventDAO')
    def test_EventBO_handle_add_command_with_alarm_time(self, MockEventDAO):
        options = {"name": "test_event",
                   "interval": 86400,
                   "alarm_time": Event.DEFAULT_ALARM_TIME}
        user = "test_user"

        MockEventDAO.has_event.return_value = False
        MockEventDAO.add_event.return_value = True
        bo = EventBO(MockEventDAO)

        result = bo.handle_add_command(user, options)
        self.assertTrue(result)

    @patch('dao.EventDAO')
    def test_EventBO_handle_add_command_without_alarm_time(self, MockEventDAO):
        options = {"name": "test_event",
                   "interval": 86400,
                   "alarm_time": Event.DEFAULT_ALARM_TIME}
        user = "test_user"

        MockEventDAO.has_event.return_value = False
        MockEventDAO.add_event.return_value = True
        bo = EventBO(MockEventDAO)

        result = bo.handle_add_command(user, options)
        self.assertTrue(result)

    @patch('dao.EventDAO')
    def test_EventBO_handle_reset_command(self, MockEventDAO):
        options = {"name": "test_event"}
        user = "test_user"

        MockEventDAO.query_event_by_target_and_name.return_value = \
            {"target": "test target",
             "name": "test event",
             "last_notified_time": 0}
        MockEventDAO.reset_event.return_value = True

        bo = EventBO(MockEventDAO)

        result = bo.handle_reset_command(user, options)
        self.assertTrue(result)

    @patch('dao.EventDAO')
    def test_EventBO_handle_remove_command(self, MockEventDAO):
        options = {"name": "test_event"}
        user = "test_user"

        MockEventDAO.remove_event.return_value = True
        bo = EventBO(MockEventDAO)

        result = bo.handle_remove_command(user, options)
        self.assertTrue(result)

    @patch('dao.EventDAO')
    @patch('message.MessageApi')
    def test_EventBO_handle_list_command(self, MockEventDAO, MockMessageApi):
        options = {}
        user = "test_user"

        MockEventDAO.query_events_by_target.return_value = [
            {
                "created_time": 1503061200,
                "last_notified_time": 1484123123,
                "name": "test_target",
                "interval": 86400}
        ]
        bo = EventBO(MockEventDAO, MockMessageApi)
        bo.handle_list_command(user, options)

    @patch('dao.EventDAO')
    @patch('message.MessageApi')
    def test_EventBO_send_notification_should_send(self, MockEventDAO, MockMessageApi):
        MockEventDAO.query_all_events.return_value = [
            {"created_time": 10000,
             "name": "test_target",
             "interval": 100,
             "target": "test_target"}
        ]
        bo = EventBO(MockEventDAO, MockMessageApi)
        bo.send_notification(current_time=10101)

        MockMessageApi.push_reset_confirm_message.assert_called_once()
        MockEventDAO.update_last_notified_time.assert_called_once()

    @patch('dao.EventDAO')
    @patch('message.MessageApi')
    def test_EventBO_send_notification_should_not_send(self, MockEventDAO, MockMessageApi):
        MockEventDAO.query_all_events.return_value = [
            {"created_time": 10000,
             "name": "test_target",
             "interval": 100,
             "target": "test_target"}
        ]
        bo = EventBO(MockEventDAO, MockMessageApi)
        bo.send_notification(current_time=10001)

        MockMessageApi.push_reset_confirm_message.assert_not_called()
        MockEventDAO.update_last_notified_time.assert_not_called()

    @patch('dao.EventDAO')
    @patch('message.MessageApi')
    def test_EventDAO_compose_alert_message_minutes(self, MockEventDAO, MockMessageApi):
        name = "test_event"
        interval = 60
        time_diff = 120

        bo = EventBO(MockEventDAO, MockMessageApi)
        output = bo.compose_alert_message(name, time_diff, interval)
        self.assertEqual(Util.compose_how_long_from_last_time_string(name, 2, "分鐘"), output)

    @patch('dao.EventDAO')
    @patch('message.MessageApi')
    def test_EventDAO_compose_alert_message_hours(self, MockEventDAO, MockMessageApi):
        name = "test_event"
        interval = 3600
        time_diff = 7200

        bo = EventBO(MockEventDAO, MockMessageApi)
        output = bo.compose_alert_message(name, time_diff, interval)
        self.assertEqual(Util.compose_how_long_from_last_time_string(name, 2, "小時"), output)

    @patch('dao.EventDAO')
    @patch('message.MessageApi')
    def test_EventDAO_compose_alert_message_days(self, MockEventDAO, MockMessageApi):
        name = "test_event"
        interval = 86400
        time_diff = 172800

        bo = EventBO(MockEventDAO, MockMessageApi)
        output = bo.compose_alert_message(name, time_diff, interval)
        self.assertEqual(Util.compose_how_long_from_last_time_string(name, 2, "天"), output)

    @patch("pymongo.MongoClient")
    def test_EventDAO_add_user_and_event(self, MockDB):
        MockDB.user_data.event.insert_one.acknowledged.return_value = True
        dao = EventDAO(MockDB)

        self.assertTrue(dao.add_user_and_event("test target", Event("test target", "test event")))

    @patch("pymongo.MongoClient")
    def test_EventDAO_update_last_notified_time(self, MockDB):
        MockDB.user_data.event.update_one.acknowledged.return_value = True
        dao = EventDAO(MockDB)

        self.assertTrue(dao.update_last_notified_time("test target", "test name", "test last_notified_time"))

    @patch("pymongo.MongoClient")
    def test_EventDAO_reset_event(self, MockDB):
        MockDB.user_data.event.update_one.acknowledged.return_value = True
        dao = EventDAO(MockDB)

        self.assertTrue(dao.reset_event({"target": "test target", \
            "name": "test event", "last_notified_time": 0, "alarm_time": Event.DEFAULT_ALARM_TIME}))

    @patch("pymongo.MongoClient")
    def test_EventDAO_has_event(self, MockDB):
        MockDB.user_data.event.find.return_value = [{"name": "test event"}]
        dao = EventDAO(MockDB)

        self.assertTrue(dao.has_event(Event("test target", "test event")))

    @patch("pymongo.MongoClient")
    def test_EventDAO_add_event(self, MockDB):
        MockDB.user_data.event.insert_one.acknowledged.return_value = True
        dao = EventDAO(MockDB)

        self.assertTrue(dao.add_event(Event("test target", "test event")))

    @patch("pymongo.MongoClient")
    def test_EventDAO_remove_event(self, MockDB):
        MockDB.user_data.event.delete_one.acknowledged.return_value = True
        dao = EventDAO(MockDB)

        self.assertTrue(dao.remove_event(Event("test target", "test event")))


if __name__ == '__main__':
    unittest.main()
