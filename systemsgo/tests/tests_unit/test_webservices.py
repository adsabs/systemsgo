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
import unittest
import requests
import re

from flask import url_for, current_app
from flask.ext.testing import TestCase
from httpretty import HTTPretty
from views import HomeView

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
            HTTPretty.HEAD,
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

class TestSystemsGo(TestCase):
    """
    A basic base class for all of the tests here
    """

    def create_app(self):
        """
        Create the wsgi application
        """
        app_ = app.create_app()
        return app_

    def test_that_homeview_returns_json_on_get(self):
        """
        Tests that the HomeView returns a JSON string with the
        expected format
        """
        url = url_for('homeview')
        with MockStatusService():
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertTrue(len(response.json) > 0)

        for entry in response.json:
            for key in ['status', 'url', 'name']:
                self.assertIn(key, entry.keys())

    @unittest.skip('Deprecated')
    def test_that_homeview_returns_filled_template(self):
        """
        Tests that the HomeView returns a correctly filled template
        """
        url = url_for('homeview')
        with MockStatusService():
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        for front_end in current_app.config['SYSTEMSGO_FRONT_END_SERVER_LIST']:
            self.assertIn('{0}</a>: online'
                          .format(front_end['name']), response.data)

    def test_the_status_of_a_service(self):
        """
        Tests the staticmethod that tests if a service is available or not
        """
        with MockStatusService(status=200):
            for front_end in current_app.config[
                'SYSTEMSGO_FRONT_END_SERVER_LIST'
            ]:
                status = HomeView.check_status(front_end['url'])
                print status, front_end['url']
                self.assertEqual(status, 'online')

    def test_batch_statuses(self):
        """
        Tests that the staticmethod that tests a bulk set of services
        """
        with MockStatusService(status=200):
            all_status = HomeView.check_bulk_status(
                current_app.config['SYSTEMSGO_FRONT_END_SERVER_LIST']
            )

        for status in all_status:
            self.assertEqual(status['status'], 'online')

    def test_that_the_batch_status_of_a_service_is_cached(self):
        """
        Tests the scenario when there is a response in the caching period
        """
        with MockStatusService(status=200):
            all_status = HomeView.check_bulk_status(
                current_app.config['SYSTEMSGO_FRONT_END_SERVER_LIST']
            )
        for status in all_status:
            self.assertEqual(status['status'], 'online')

        with MockStatusService(status=400):
            all_status = HomeView.check_bulk_status(
                current_app.config['SYSTEMSGO_FRONT_END_SERVER_LIST']
            )
        for status in all_status:
            self.assertEqual(status['status'], 'online')

    def test_mock_of_status_service(self):
        """
        Tests that a mock service gives a 200 or 400 response based on the
        users supplied kwargs.
        """
        with MockStatusService():
            response = requests.head('http://fakeurl.com')
        self.assertEqual(response.status_code, 200)

        with MockStatusService(status=400):
            response = requests.head('http://fakeurl.com')
        self.assertEqual(response.status_code, 400)

    def test_root_returns_index(self):
        """
        Tests that the root path returns the index html. This is a temporary
        hack for testing simply.
        """
        url = url_for('indexview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'Status page of the front end web services.' in response.data
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
