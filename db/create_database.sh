#!/bin/bash

curl -XPUT http://localhost:9200/public_titles # -d @mapping.json

curl -XPUT http://localhost:9200/authenticated_titles # -d @mapping.json

