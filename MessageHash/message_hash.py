# !/usr/bin/env python

import hashlib
import base64

class MessageHash(object):
    """Class used to create hashes of messages."""

    @staticmethod
    def sha256(message):
        return hashlib.sha256(message.encode()).hexdigest()