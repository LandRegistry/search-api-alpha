#!/bin/bash

MAPLOC="$(dirname $0)"

curl -XPUT http://localhost:9200/public_titles -d @${MAPLOC}/mapping.json

curl -XPUT http://localhost:9200/authenticated_titles -d @${MAPLOC}/mapping.json

