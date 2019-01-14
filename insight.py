from flask import Flask
from flask_caching import Cache
from flask.cli import main

import logging, os

LOG_FILENAME = 'insight.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

application = Flask(__name__)
application.secret_key = os.getenv('SECRET_KEY')
cache = Cache(application, config={'CACHE_TYPE': 'simple'})

if __name__ == '__main__':
    main(as_module=False)
