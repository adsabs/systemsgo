# encoding: utf-8
"""
Application factory
"""

import logging.config
from views import HomeView
from flask import Flask
from flask.ext.cors import CORS
from flask.ext.restful import Api
from cache import cache
from flask.ext.consulate import Consul, ConsulConnectionError

def create_app():
    """
    Create the application and return it to the user

    :return: flask.Flask application
    """
    app = Flask(__name__, static_folder=None)
    app.url_map.strict_slashes = False

    # Load config and logging
    Consul(app)  # load_config expects consul to be registered
    load_config(app)
    logging.config.dictConfig(
        app.config['SYSTEMSGO_LOGGING']
    )

    # Cache
    cache.init_app(app, config=app.config['CACHE'])

    # CORS
    CORS(app, resource={r'/status': {'origins': 'localhost'}})
    # Register extensions
    api = Api(app)

    # Add end points
    api.add_resource(HomeView, '/status')

    return app


def load_config(app):
    """
    Loads configuration in the following order:
        1. config.py
        2. local_config.py (ignore failures)
        3. consul (ignore failures)
    :param app: flask.Flask application instance
    :return: None
    """

    app.config.from_pyfile('config.py')

    try:
        app.config.from_pyfile('local_config.py')
    except IOError:
        app.logger.warning('Could not load local_config.py')

    try:
        app.extensions['consul'].apply_remote_config()
    except ConsulConnectionError as error:
        app.logger.warning('Could not apply config from consul: {error}'
                           .format(error=error))

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, use_reloader=False)
