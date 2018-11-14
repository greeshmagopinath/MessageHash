#!/usr/bin/env python

import os
import tornado.ioloop
import tornado.web
import json

from redis import Redis
from MessageHash.message_hash import MessageHash
from MessageHash.store import Store

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

redis = Redis(host='redis', port=6379)
store = Store(redis)

try:
    scheme = os.environ['SCHEME']
    ip_address = os.environ['IP_ADDRESS']
    port = os.environ['PORT']
except KeyError:
    scheme = 'http'
    ip_address = 'localhost'
    port = 8080

class MainHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(max_workers=5)

    def __create_message_digest(self, message):
        digest = MessageHash.sha256(message)
        store.keep(digest, message)
        return digest

    @run_on_executor
    def background_task(self, message):
        if message:
            response = {
                "digest" : self.__create_message_digest(message)
            }
            return 201, json.dumps(response, sort_keys=True)
        else:
            response = {
                'err_msg': 'Please post a valid message'
            }
            return 400, json.dumps(response, sort_keys=True)

    @tornado.gen.coroutine
    def post(self):
        message = self.get_argument('message',None)
        status_code, result = yield self.background_task(message)
        self.set_status(status_code)
        self.write(result)

    def get(self, *args):
        if len(args) == 1:
            hash = args[0]
            message = store.value_of(hash)
            if message:
                response = {
                    "message" : message
                }
                self.set_status(200)
                return self.write(json.dumps(response, sort_keys=True))
            else:
                response = {
                    'err_msg': "Message not found"
                }
                self.set_status(404)
                return self.write(json.dumps(response, sort_keys=True))
        else:
            response = {
                'err_msg': 'Please set only one argument path'
            }
            self.set_status(400)
            return self.write(json.dumps(response, sort_keys=True))


def main():
    app = tornado.web.Application([(r'/messages/', MainHandler), (r'/messages/(.*)', MainHandler)], debug=False)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()