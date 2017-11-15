import os

import psycopg2
from flask import g

from flask import Flask
from werkzeug.contrib.cache import MemcachedCache

app = Flask(__name__)

# TICKET STATUSES
OPEN = 'open'
WAITING_ANSWER = 'waiting'
ANSWERED = 'answered'
CLOSED = 'closed'

ticket_status_path = {
    OPEN: [ANSWERED, CLOSED],
    ANSWERED: [WAITING_ANSWER, CLOSED],
    WAITING_ANSWER: [ANSWERED, CLOSED],
    CLOSED: []
}

POSTGRES_URL = os.getenv('POSTGRES_URL')
MEMCACHED_URL = os.getenv('MEMCACHED_URL')


def get_db():
    if not hasattr(g, 'conn'):
        g.conn = psycopg2.connect(POSTGRES_URL)
    return g.conn


def get_cache():
    if not hasattr(g, 'cache'):
        g.cache = MemcachedCache([MEMCACHED_URL])
    return g.cache


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'conn'):
        g.conn.close()
