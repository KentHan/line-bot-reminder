#!/usr/bin/env python

"""Tests for the Flask Heroku template."""

import unittest
from app import app
from app import command_parser

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


if __name__ == '__main__':
    unittest.main()
