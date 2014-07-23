import os, logging
from flask import Flask

app = Flask(__name__)

app.config.from_object(os.environ.get('SETTINGS'))

app.logger.info("\nConfiguration\n%s\n" % app.config)

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
