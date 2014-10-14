#!/bin/bash
HOST=${1:-"localhost:9200"}
curl -XDELETE http://$HOST/public_titles
curl -XDELETE http://$HOST/authenticated_titles
