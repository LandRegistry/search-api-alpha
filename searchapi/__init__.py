import os, logging
from flask import Flask
from raven.contrib.flask import Sentry

app = Flask(__name__)

app.config.from_object(os.environ.get('SETTINGS'))

app.logger.debug("\nConfiguration\n%s\n" % app.config)

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

# Sentry exception reporting
if 'SENTRY_DSN' in os.environ:
    sentry = Sentry(app, dsn=os.environ['SENTRY_DSN'])

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
