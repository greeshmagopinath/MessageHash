===========
MessageHash
===========

.. image:: https://codecov.io/gh/greeshmagopinath/MessageHash/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/greeshmagopinath/MessageHash
    :alt: Codecov

+-------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
|                                Linux                                                      |                                       Windows                                    |
+===========================================================================================+==================================================================================+
| .. image:: https://api.travis-ci.org/greeshmagopinath/MessageHash.svg?branch=master       | .. image:: https://ci.appveyor.com/api/projects/status/jiah44pbhpo1osfm?svg=true |
|    :target: https://travis-ci.org/greeshmagopinath/MessageHash                            |    :target: https://ci.appveyor.com/project/greeshmagopinath/messagehash         |
|    :alt: Travis-Ci                                                                        |    :alt: AppVeyor                                                                |
+-------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------+

============
Introduction
============

Message Hashing service using `Tornado` and `Redis` runs on `Docker`.

================
Getting the code
================

The code is hosted at https://github.com/greeshmagopinath/MessageHash

Check out the latest development version anonymously with::

    $ git clone git://github.com/greeshmagopinath/MessageHash.git
    $ cd MessageHash

To install dependencies, run either::

    $ pip install -Ur requirements.testing.txt
    $ pip install -Ur requirements.txt

To install the minimal dependencies for production use run::

    $ pip install -Ur requirements.txt

=============
Running Tests
=============

The test suite can be run against a single Python version which requires ```pip install pytest``` and optionally ```pip install pytest-cov``` (these are included if you have installed dependencies from ```requirements.testing.txt```)

To run the unit tests with a single Python version::

    $ py.test -v

to also run code coverage::

    $ py.test -v --cov-report xml --cov=MessageHash

To run the unit tests against a set of Python versions::

    $ tox

========
Commands
========

---
Run
---

Running up in Docker

.. code::

    docker-compose up

Running in Kubernetes

- For testing you can run **message_hash** in **Kubernetes** with using **Docker**. Run docker and then the following commands should work for you.

.. code::

    # Use Docker for minikube
    eval $(minikube docker-env)

    # Create developments and pods
    kubectl create -f deployment-redis.yml
    kubectl create -f deployment-message_hash.yml

    # Create services
    kubectl create -f service-redis.yml
    kubectl create -f service-message_hash.yml

    # Get url for **message_hash**
    minikube service message_hash --message

------------
Sample Usage
------------

.. code::

    # Hash a message with POST
    curl -X POST -H "Content-Type:application/json" -d '{ "message":"foo"}'  http://127.0.0.1:8080/messages

    # Response
    {
        "digest": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"
    }


    # Error case with null message
    curl -X POST -H "Content-Type:application/json" -d '{ "message":""}'  http://127.0.0.1:8080/messages

    # Response
    {
        "err_msg": "Please post a valid message"
    }


    # Retrieve the original message with GET
    curl -i http://127.0.0.1/messages/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae

    # Response
    {
        "message": "foo"
    }


    # Error case with invalid digest
    curl -i http://127.0.0.1/messages/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

    # Response
    {
        "err_msg": "Message not found"
    }
