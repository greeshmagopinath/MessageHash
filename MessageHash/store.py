#!/usr/bin/env python

from redis import (
    Redis,
    exceptions
)

class Store(object):
    """ Class used to store messages and digests."""

    def __init__(self, redis):
        self._redis = redis

    def keep(self, key, value):
        try:
            self._redis.set(key,value)
        except exceptions.ConnectionError:
            print('Unable to connect to Redis server when trying to store message')

    def value_of(self,key):
        try:
            message = self._redis.get(key)
            if message:
                return message.decode('utf-8')
            return None
        except exceptions.ConnectionError:
            print('Unable to connect to Redis server when trying to retrieve message')
            return None