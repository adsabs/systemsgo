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
    def get(self):
        """
        HTTP GET Request
        """
        response_list = [
            dict(
                name='Bumblebee',
                status='Online'
            )
        ]

        # # Check the status using the staticmethod
        # for service in current_app.config['SYSTEMSGO_FRONT_END_SERVER_LIST']:
        #     status = self.check_status(service)
        #     service['status'] = status

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