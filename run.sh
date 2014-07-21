#!/bin/bash

export SETTINGS='config.DevelopmentConfig'
export ELASTICSEARCH_HOST='localhost'
export ELASTICSEARCH_PORT='9200'

python run_dev.py
