#!/bin/bash

export SETTINGS='config.DevelopmentConfig'
export SEARCH_API_URL='http://localhost:8003'
export ES_URI = os.environ.get('http://localhost:9200')

python run_dev.py
