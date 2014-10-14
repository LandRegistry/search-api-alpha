#!/bin/bash

MAPLOC="$(dirname $0)"
HOST=${1:-"localhost:9200"}
curl -XPUT http://$HOST/public_titles -d @${MAPLOC}/mapping.json

curl -XPUT http://$HOST/authenticated_titles -d @${MAPLOC}/mapping.json

