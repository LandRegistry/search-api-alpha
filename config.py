import os

class Config(object):
    DEBUG = False
    ELASTICSEARCH_HOST = os.environ['ELASTICSEARCH_HOST']
    ELASTICSEARCH_PORT = os.environ['ELASTICSEARCH_PORT']
    ELASTICSEARCH_USESSL = os.environ['ELASTICSEARCH_USESSL']
    ELASTICSEARCH_USERPASS = os.environ['ELASTICSEARCH_USERPASS']

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True
