# encoding: utf-8
"""
Views
"""

import json
import requests
import datetime

from flask import current_app, request, render_template, make_response
from flask.ext.restful import Resource
from utils import get_post_data, err
from cache import cache

class HomeView(Resource):
    """
    Return the home page template with the content filled.
    """
    @staticmethod
    def check_status(url):
        """
        Checks the status of a given website with its URL. This should be
        cached so that it does not repeatedly spam a site with requests.
        :param url: url of the website to check the status

        :return: 'Online' is response, 'Offline' is unresponsive
        """
        response = requests.get(url)
        if response.status_code == 200:
            return 'Online'
        else:
            return 'Offline'

    def get(self):
        """
        HTTP GET Request

        An index page is rendered and returned
        """
        # Make a copy of the config file so that it can be modified, but does
        # not affect elsewhere
        response_list = current_app.config[
            'SYSTEMSGO_FRONT_END_SERVER_LIST'
        ][:]

        # Check the status using the staticmethod
        for service in response_list:
            status = HomeView.check_status(service['url'])
            service['status'] = status

        # Return the filled template
        return make_response(
            render_template('index.html', response_list=response_list),
            200,
            {'Content-Type': 'text/html'}
        )

class CachedTime(Resource):
    """
    Return time but cached for 1 minute
    """
    @cache.cached(timeout=3)
    def get(self):
        """
        HTTP GET request
        :return: datetime object
        """

        return {'time': datetime.datetime.utcnow().isoformat()}, 200