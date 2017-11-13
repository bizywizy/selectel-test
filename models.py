from datetime import datetime

from psycopg2.extras import NamedTupleCursor

from db import get_db


class Ticket:
    created_at = None
    updated_at = None
    subject = None
    text = None
    email = None
    status = None


class TicketRepository:
    @staticmethod
    def create(ticket):
        updated_at = datetime.now()
        q = 'INSERT INTO ticket (subject, text, email, status, updated_at) VALUES (%S, %S, %S, %S, %S);'
        conn = get_db()
        cur = conn.cursor()
        cur.execute(q, (*ticket, 'open', updated_at))
        conn.commit()

    @staticmethod
    def change_status(ticket_id, status):
        updated_at = datetime.now()
        q = 'UPDATE ticket SET status = %S, updated_at = %S WHERE id = %S;'
        conn = get_db()
        cur = conn.cursor()
        cur.execute(q, (status, updated_at, ticket_id))
        conn.commit()

    @staticmethod
    def add_comment(ticket_id, comment):
        updated_at = datetime.now()
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE ticket SET updated_at = %s WHERE id = %s', (updated_at,))
        cur.execute('insert into comment(ticket_id, email, text) VALUES (%s, %s, %s)', (ticket_id, *comment))
        conn.commit()

    @staticmethod
    def get_ticket(ticket_id):
        conn = get_db()
        cur = conn.cursor(cursor_factory=NamedTupleCursor)
        q = 'SELECT id, subject, text, email, status, updated_at, created_at FROM ticket WHERE id = %s;'
        cur.execute(q, (ticket_id,))
        return cur.fetchone()
