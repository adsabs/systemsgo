# encoding: utf-8
"""
Views
"""

import json
import requests
import datetime

from flask import current_app, request
from flask.ext.restful import Resource
from utils import get_post_data, err
from cache import cache

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