import os

class Config(object):
    DEBUG = False
    ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST')
    ELASTICSEARCH_PORT = os.environ.get('ELASTICSEARCH_PORT')
    ELASTICSEARCH_USESSL = os.environ.get('ELASTICSEARCH_USESSL')
    ELASTICSEARCH_USERPASS = os.environ.get('ELASTICSEARCH_USERPASS')

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True
    ELASTICSEARCH_HOST = 'localhost'
    ELASTICSEARCH_PORT = '9200'
    ELASTICSEARCH_USESSL = ''
    ELASTICSEARCH_USERPASS = ''

class DockerConfig(object):
    DEBUG = True
    ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_1_PORT_9200_TCP_ADDR')
    ELASTICSEARCH_PORT = os.environ.get('ELASTICSEARCH_1_PORT_9200_TCP_PORT')
    ELASTICSEARCH_USESSL = ''
    ELASTICSEARCH_USERPASS = '' 


