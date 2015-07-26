# encoding: utf-8
"""
Views
"""

import urllib
from flask import current_app, render_template, make_response
from flask.ext.restful import Resource
from cache import cache

MINUTES = 60.0  # seconds
SYSTEMSGO_CACHE_TIMEOUT = 5*MINUTES

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

        # which is faster? requests or urllib?
        status_code = urllib.urlopen(url).getcode()

        if status_code == 200:
            return 'online'
        else:
            return 'offline'

    @staticmethod
    @cache.cached(timeout=SYSTEMSGO_CACHE_TIMEOUT)
    def check_bulk_status(service_list):
        """
        Checks the status of a list of services, and returns a blob with the
        response, updating the dictionary to include the status. This should
        allow simpler caching of the response into a single blob.

        :param service_list: a list of dictionaries, which contains the
                             keywords: 'name', 'url'
        :return: keyword 'status' is added to the service_list
        """
        response = service_list[:]
        for service in response:
            service['status'] = HomeView.check_status(service['url'])
        return response

    def get(self):
        """
        HTTP GET Request

        An index page is rendered and returned
        """

        # Check the status using the staticmethod
        response_list = HomeView.check_bulk_status(
            current_app.config['SYSTEMSGO_FRONT_END_SERVER_LIST'][:]
        )

        # Return the filled template
        return response_list, 200