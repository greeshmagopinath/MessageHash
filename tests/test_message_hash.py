#!/usr/bin/env python

import unittest
from MessageHash import MessageHash

class MessageHashTest(unittest.TestCase):
    """Class to test hashing of messages"""

    def test_sha256(self):
        text = MessageHash.sha256('foo')
        self.assertEqual(text, '2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae')