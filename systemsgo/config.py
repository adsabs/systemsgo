# encoding: utf-8
"""
Configuration file. Please prefix application specific config values with
the application name.
"""

# Front end server list
SYSTEMSGO_FRONT_END_SERVER_LIST = [
    {
        'name': 'Bumblebee',
        'url': 'https://ui.adsabs.harvard.edu'
    },
    {
        'name': 'Hourly',
        'url': 'http://hourly.adslabs.org'
    },
    {
        'name': 'API',
        'url': 'https://api.adsabs.harvard.edu/status'
    },
    {
        'name': 'ADS 2.0 (BEER)',
        'url': 'http://labs.adsabs.harvard.edu/adsabs/'
    },
    {
        'name': 'ADS Classic',
        'url': 'http://adsabs.harvard.edu/'
    }
]

# Cache settings
CACHE = {'CACHE_TYPE': 'simple'}
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
