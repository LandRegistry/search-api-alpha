#!/bin/bash

curl -XDELETE https://$HOST/public_titles
curl -XDELETE https://$HOST/authenticated_titles

curl -XPUT https://$HOST/public_titles
curl -XPUT https://$HOST/authenticated_titles

curl -XPUT http://$HOST/_all/_mapping/titles -d @${MAPLOC}/mapping.json
