#!/bin/bash

export SETTINGS='config.DevelopmentConfig'
export SEARCH_API_URL='http://localhost:8003'
export ELASTICSEARCH_HOST='localhost'
export ELASTICSEARCH_PORT='9200'

python run_dev.py
