#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mock import patch

from app import app
from app import command_parser
from bo import EventBO
from event import Event

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

    def test_default_redirecting(self):
        rv = self.app.get('/about')
        self.assertEqual(rv.status_code, 301)

    def test_404_page(self):
        rv = self.app.get('/i-am-not-found/')
        self.assertEqual(rv.status_code, 404)

    def test_static_text_file_request(self):
        rv = self.app.get('/robots.txt')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)
        rv.close()

    def test_input_add_parameters(self):
        input = "/add clean 86400 21:00"
        output_options = command_parser(input)
        self.assertEqual(output_options, {"name": "clean", 
                                            "interval": "86400", 
                                            "alarm_time": "21:00"})

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
                    "alarm_time": "21:00"}
        user = "test_user"

        MockEventDAO.has_event.return_value = False
        MockEventDAO.add_event.return_value = True
        bo = EventBO(MockEventDAO)

        result = bo.handle_add_command(user, options)
        self.assertTrue(result)

    @patch('dao.EventDAO')
    def test_EventBO_handle_add_command_without_alarm_time(self, MockEventDAO):
        options = {"name": "test_event",
                    "interval": 86400}
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

        MockEventDAO.reset_command.return_value = True
        bo = EventBO(MockEventDAO)

        result = bo.handle_reset_command(user, options)
        self.assertTrue(False)

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
                {"last_notified_time": 1484123123, 
                    "name": "test_target", 
                    "interval": 86400}
            ]
        bo = EventBO(MockEventDAO, MockMessageApi)
        bo.handle_list_command(user, options)

    @patch('dao.EventDAO')
    @patch('message.MessageApi')
    def test_EventBO_send_notification(self, MockEventDAO, MockMessageApi):
        MockEventDAO.query_all_events.return_value = [
                {"last_notified_time": 1484123123, 
                    "name": "test_target", 
                    "interval": 86400,
                    "created_time": 1484123123,
                    "target": "test_target"}
            ]
        bo = EventBO(MockEventDAO, MockMessageApi)
        bo.send_notification()

    @patch('dao.EventDAO')
    @patch('message.MessageApi')
    def test_EventDAO_compose_alert_message_minutes(self, MockEventDAO, MockMessageApi):
        name = "test_event"
        interval = 60
        time_diff = 120

        bo = EventBO(MockEventDAO, MockMessageApi)
        output = bo.compose_alert_message(name, time_diff, interval)
        self.assertEqual(output, "離上一次\"test_event\"已經2分鐘了！")

    @patch('dao.EventDAO')
    @patch('message.MessageApi')
    def test_EventDAO_compose_alert_message_hours(self, MockEventDAO, MockMessageApi):
        name = "test_event"
        interval = 3600
        time_diff = 7200

        bo = EventBO(MockEventDAO, MockMessageApi)
        output = bo.compose_alert_message(name, time_diff, interval)
        self.assertEqual(output, "離上一次\"test_event\"已經2小時了！")


    @patch('dao.EventDAO')
    @patch('message.MessageApi')
    def test_EventDAO_compose_alert_message_days(self, MockEventDAO, MockMessageApi):
        name = "test_event"
        interval = 86400
        time_diff = 172800

        bo = EventBO(MockEventDAO, MockMessageApi)
        output = bo.compose_alert_message(name, time_diff, interval)
        self.assertEqual(output, "離上一次\"test_event\"已經2天了！")

if __name__ == '__main__':
    unittest.main()
