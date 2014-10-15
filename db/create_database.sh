#!/bin/bash

HOST=${1:-"localhost:9200"}
curl -XPUT http://$HOST/public_titles

curl -XPUT http://$HOST/authenticated_titles

