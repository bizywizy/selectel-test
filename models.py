from collections import namedtuple
from datetime import datetime

from app import get_db, get_cache, ticket_status_path, CLOSED
from utils import build_ticket_name

Ticket = namedtuple('Ticket', ('subject', 'text', 'email'))
Comment = namedtuple('Comment', ('email', 'text'))
_ = namedtuple('_', ('id', 'subject', 'text', 'email', 'status', 'updated_at', 'created_at'))


class WrongStatusException(BaseException):
    pass


class TicketRepository:
    @staticmethod
    def create(ticket):
        updated_at = datetime.now()
        q = 'INSERT INTO ticket (subject, text, email, status, updated_at) VALUES (%s, %s, %s, %s, %s);'
        conn = get_db()
        cur = conn.cursor()
        cur.execute(q, (*ticket, 'open', updated_at))
        conn.commit()

    @staticmethod
    def change_status(ticket, new_status):
        if new_status not in ticket_status_path.get(ticket.status, []):
            raise WrongStatusException()
        updated_at = datetime.now()
        q = 'UPDATE ticket SET status = %s, updated_at = %s WHERE id = %s;'
        conn = get_db()
        cur = conn.cursor()
        cur.execute(q, (new_status, updated_at, ticket.id))
        cache = get_cache()
        cache.delete(build_ticket_name(ticket.id))
        conn.commit()

    @staticmethod
    def add_comment(ticket, comment):
        if ticket.status == CLOSED:
            raise WrongStatusException()
        updated_at = datetime.now()
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE ticket SET updated_at = %s WHERE id = %s', (updated_at,))
        cur.execute('INSERT INTO comment(ticket_id, email, text) VALUES (%s, %s, %s)', (ticket.id, *comment))
        cache = get_cache()
        cache.delete(build_ticket_name(ticket.id))
        conn.commit()

    @staticmethod
    def get_ticket(ticket_id):
        ticket_name = build_ticket_name(ticket_id)
        cache = get_cache()
        if cache.has(ticket_name):
            return cache.get(ticket_name)
        conn = get_db()
        cur = conn.cursor()
        q = 'SELECT id, subject, text, email, status, updated_at, created_at FROM ticket WHERE id = %s;'
        cur.execute(q, (ticket_id,))
        ticket = cur.fetchone()
        if not ticket:
            return
        ticket = _(*ticket)
        cache.set(ticket_name, ticket)
        return ticket
