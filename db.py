import psycopg2
from flask import g

from main import app


def get_db():
    if not hasattr(g, 'conn'):
        g.conn = psycopg2.connect('dbname=selectel_test user=selectel_user password=qwerty')
    return g.conn


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'conn'):
        g.conn.close()
