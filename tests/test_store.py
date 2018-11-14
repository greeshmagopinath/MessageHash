#!/usr/bin/env/python

import unittest
import fakeredis
from MessageHash.store import Store

class StoreTest(unittest.TestCase):
    """Class to test storage of digests and messages"""

    def setUp(self):
        self.redis = fakeredis.FakeStrictRedis()
        self.store = Store(self.redis)

    def test_initiation(self):
        self.assertIsNotNone(self.store)

    def test_keep(self):
        self.store.keep('key','value')
        value = self.store.value_of('key')
        self.assertEqual(value, 'value')