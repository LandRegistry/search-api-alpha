import os, logging
from flask import Flask

app = Flask(__name__)

# to run the app set an environment variable called SETTINGS
# the value should be set to one of the classes in config.py
# e.g. export SETTINGS="config.TestConfig"
# or heroku config:set SETTINGS=config.HerokuConfig
app.config.from_object(os.environ.get('SETTINGS'))

print "============"
print app.config
print "============"

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
