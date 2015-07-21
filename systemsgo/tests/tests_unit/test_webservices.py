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
import re

from flask import url_for, current_app
from flask.ext.testing import TestCase
from httpretty import HTTPretty
from views import CachedTime, HomeView

class MockStatusService(object):
    """
    Mock of the ADSWS API
    """
    def __init__(self, status=200):
        """
        Constructor
        :param status: status to return
        """
        self.status = status

        def request_callback(request, uri, headers):
            """
            :param request: HTTP request
            :param uri: URI/URL to send the request
            :param headers: header of the HTTP request
            :return:
            """
            # This should ensure that it should fail on the second call
            return self.status, headers, {}

        HTTPretty.register_uri(
            HTTPretty.GET,
            re.compile('.*'),
            body=request_callback,
            content_type='application/json'
        )

    def __enter__(self):
        """
        Defines the behaviour for __enter__
        :return: no return
        """
        HTTPretty.enable()

    def __exit__(self, etype, value, traceback):
        """
        Defines the behaviour for __exit__
        :param etype: exit type
        :param value: exit value
        :param traceback: the traceback for the exit
        :return: no return
        """
        HTTPretty.reset()
        HTTPretty.disable()

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
        self.assertEqual(response3.status_code, 200)
        # self.assertIn('Offline', response3.data)

class TestUnitFlow(TestBase):
    """
    General unit tests
    """
    def test_that_homeview_returns_filled_template(self):
        """
        Tests that the HomeView returns a correctly filled template
        """
        url = url_for('homeview')
        with MockStatusService():
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        for front_end in current_app.config['SYSTEMSGO_FRONT_END_SERVER_LIST']:
            self.assertIn('{0}: Online'
                          .format(front_end['name']), response.data)

    def test_the_status_of_a_service(self):
        """
        Tests the staticmethod that tests if a service is available or not
        """
        with MockStatusService():
            for front_end in current_app.config[
                'SYSTEMSGO_FRONT_END_SERVER_LIST'
            ]:
                status = HomeView.check_status(front_end['url'])
                self.assertEqual(status, 'Online')

    @unittest.skip('Not implemented')
    def test_that_the_status_of_a_service_is_cached(self):
        """
        Tests the scenario when there is a response in the caching period
        """
        self.fail()

    def test_mock_of_status_service(self):
        """
        Tests that a mock service gives a 200 or 400 response based on the
        users supplied kwargs.
        """
        with MockStatusService():
            response = requests.get('http://fakeurl.com')
        self.assertEqual(response.status_code, 200)

        with MockStatusService(status=400):
            response = requests.get('http://fakeurl.com')
        self.assertEqual(response.status_code, 400)

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
