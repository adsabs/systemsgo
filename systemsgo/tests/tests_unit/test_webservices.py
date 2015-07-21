# coding: utf-8
"""
Test webservices
"""

import sys
import os
PROJECT_HOME = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(PROJECT_HOME)

import app
import json
import time
import unittest
import requests

from flask import url_for, current_app
from flask.ext.testing import TestCase
from httpretty import HTTPretty
from views import CachedTime

class TestBase(TestCase):
    """
    A basic base class for all of the tests here
    """

    def create_app(self):
        """
        Create the wsgi application
        """
        app_ = app.create_app()
        return app_

class TestFunctionalWorkFlow(TestBase):
    """
    Outlines the use of the service from the view point of a user, which will
    allow other tests to be decided upon.
    """

    def test_functional(self):
        """
        Basic usage by a user. Selenium tests would be nice, but they depend
        upon having a binary in the repo, which I'm not wanting to do.
        """

        # The user visits the web page
        url = url_for('homeview')
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)

        # The user finds a list of sites that they ADS supplies, and sees
        # that they are all active
        self.assertIn('Online', response1.data)
        self.assertNotIn('Offline', response1.data)

        # The user re-visits the site, but nothing has changed, given that
        # the site is cached
        response2 = self.client.get(url)
        self.assertEqual(response1.data, response2.data)

        # The user waits a given time for the cache to empty, and then revisits
        # finding that some sites are now unresponsive
        response3 = self.client.get(url)
        self.assertIn('Offline', response3.data)

class TestCachedTime(TestBase):
    """
    Class to test the CachedTime
    """

    def test_timed_cache(self):
        """
        Test that the time is cached every 3 seconds
        """
        url = url_for('cachedtime')
        get_time = lambda: self.client.get(url).json['time']

        time_1 = get_time()
        time_2 = get_time()
        time_3 = get_time()
        time.sleep(4)

        self.assertEqual(time_1, time_2)
        self.assertEqual(time_2, time_3)
        self.assertNotEqual(time_1, get_time())

if __name__ == '__main__':
    unittest.main(verbosity=2)
