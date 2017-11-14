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


def get_db():
    if not hasattr(g, 'conn'):
        g.conn = psycopg2.connect('dbname=selectel_test user=selectel_user password=qwerty host=localhost')
    return g.conn


def get_cache():
    if not hasattr(g, 'cache'):
        g.cache = MemcachedCache(['127.0.0.1:11211'])
    return g.cache


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'conn'):
        g.conn.close()
