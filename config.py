import os

class Config(object):
    DEBUG = False
    ELASTICSEARCH_URI = os.environ.get('ELASTICSEARCH_URI')

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True
