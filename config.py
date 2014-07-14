import os

class Config(object):
    DEBUG = False
    SYSTEM_OF_RECORD_URI = os.environ.get('SYSTEM_OF_RECORD_URI', 'http://localhost:8000')
    ES_URI = os.environ.get('ELASTICSEARCH_URI', 'http://localhost:9200')
    # If DATABASE_URL not set fall back to sqlite db

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = 'a very secret thing indeed'

class HerokuConfig(Config):
    # db config from Config will do, but set any other env vars
    # specific to heroku here
    pass

class DevelopmentConfig(Config):
    # use this for local dev in fig+docker world
    DEBUG = True

    # format is dialect+driver://username:password@host:port/database
    SYSTEM_OF_RECORD_URI = os.environ.get('SYSTEM_OF_RECORD_URI', 'http://localhost:8000')
    ES_URI = os.environ.get('ELASTICSEARCH_URI', 'http://localhost:9200')


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SYSTEM_OF_RECORD_URI = os.environ.get('SYSTEM_OF_RECORD_URI', 'http://localhost:8000')
    ES_URI = os.environ.get('ELASTICSEARCH_URI', 'http://localhost:9200')
