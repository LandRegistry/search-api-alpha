#!/bin/bash
MAPLOC="$(dirname $0)"
HOST=${1:-"localhost:9200"}
curl -XPUT http://$HOST/public_titles

curl -XPUT http://$HOST/authenticated_titles

curl -XPUT http://$HOST/_all/_mapping/titles -d @${MAPLOC}/mapping.json

