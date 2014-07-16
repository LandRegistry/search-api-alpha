import os

class Config(object):
    DEBUG = False
    SYSTEM_OF_RECORD_URI = os.environ.get('SYSTEM_OF_RECORD_URI')
    ES_URI = os.environ.get('ELASTICSEARCH_URI')

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True
    SYSTEM_OF_RECORD_URI = os.environ.get('http://localhost:8000')
    ES_URI = os.environ.get('http://localhost:9200')
