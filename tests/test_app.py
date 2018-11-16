#!/usr/bin/env/python

import os
import tornado.web

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from MessageHash import (
    MainHandler
)

class AppTest(AsyncHTTPTestCase):

    def setUp(self):
        super(AppTest, self).setUp()
        # allow more time before timeout since we are doing remote access..
        os.environ["ASYNC TEST TIMEOUT"] = str(20)

    def get_app(self):
        return Application([(r'/messages', MainHandler), (r'/messages/(.*)', MainHandler)], debug=True, autoreload=False)

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()

    def test_digest(self):
        body = {'message': 'foo'}
        response = self.fetch(r'/messages', method='POST', body=body)
        self.assertEqual(response.code, 201)
        self.assertEqual(response.body, b'{"digest" : "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"}')

    def test_digest_empty(self):
        body = {'key' : 'foo'}
        response = self.fetch(r'/messages', method='POST', body=body)
        self.assertEqual(response.code, 400)
        self.assertEqual( response.body, b'{"err_msg" : "Please post a valid message"}')

    def test_digest_unsupported(self):
        body = {'key': 'foo'}
        response = self.fetch(r'/', method='PATCH', body=body)
        self.assertEqual(response.code, 405)

    def test_get(self):
        response = self.fetch('/messages/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae', method = 'GET')
        self.assertEqual(response.code, 201)
        self.assertEqual(response.body, b'{"message" : "foo"}')

    def test_invalid_get(self):
        response = self.fetch('/messages/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', method = 'GET')
        self.assertEqual(response.code, 404)
        self.assertEqual(response.body, b'{"err_msg": "Message not found"}')