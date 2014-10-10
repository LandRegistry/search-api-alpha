#!/bin/bash

curl -XDELETE http://localhost:9200/public_titles
curl -XDELETE http://localhost:9200/authenticated_titles
