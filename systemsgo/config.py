# encoding: utf-8
"""
Configuration file. Please prefix application specific config values with
the application name.
"""

# import os

# Front end server list
SYSTEMSGO_FRONT_END_SERVER_LIST = [
    {
        'name': 'Bumblebee',
        'url': 'https://ui.adsabs.harvard.edu',
        'img': '/static/imgs/bumblebee.png'
    },
    {
        'name': 'ADS Webservices API',
        'url': 'https://api.adsabs.harvard.edu/status',
        'img': '/static/imgs/bumblebee.png'
    },
    {
        'name': 'ADS Labs (ADS 2.0)',
        'url': 'http://labs.adsabs.harvard.edu/adsabs/',
        'img': '/static/imgs/adslabs.jpg'
    },
    {
        'name': 'ADS Classic',
        'url': 'http://adsabs.harvard.edu/',
        'img': '/static/imgs/adsclassic.png'
    }
]

# Cache settings
CACHE = {
    'CACHE_TYPE': 'simple'
    # 'CACHE_TYPE': 'memcached',
    # 'CACHE_MEMCACHED': os.environ.get('MEMCACHIER_SERVERS', '').split(','),
    # 'CACHE_MEMCACHED_USERNAME': os.environ.get('MEMCACHIER_USERNAME', ''),
    # 'CACHE_MEMCACHED_PASSWORD': os.environ.get('MEMCACHIER_PASSWORD', '')
}
SYSTEMSGO_CACHE_TIMEOUT = 10  # seconds

# Log settings
SYSTEMSGO_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s\t%(process)d '
                      '[%(asctime)s]:\t%(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        }
    },
    'handlers': {
        'file': {
            'formatter': 'default',
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/tmp/systemsgo.log',
        },
        'console': {
            'formatter': 'default',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
