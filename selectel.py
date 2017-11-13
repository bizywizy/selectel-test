from collections import namedtuple

from flask import request, Response, jsonify

from main import app
from models import TicketRepository

ticket_status_path = {
    'open': ['answered', 'closed'],
    'answered': ['waiting_answer', 'closed'],
    'waiting_answer': ['answered', 'closed'],
    'closed': []
}


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/tickets', methods=('GET', 'POST'))
def tickets():
    if request.method == 'GET':
        return 'tickets'
    if request.method == 'POST':
        data = request.json
        Ticket = namedtuple('Ticket', ('subject', 'text', 'email'))
        ticket = Ticket(data.get('subject'), data.get('text'), data.get('email'))
        TicketRepository.create(ticket)
        return Response(status=200)


@app.route('/tickets/<int:ticket_id>', methods=('GET', 'PUT'))
def ticket(ticket_id):
    if request.method == 'GET':
        ticket = TicketRepository.get_ticket(ticket_id)
        if not ticket:
            return Response(status=404)
        return jsonify(ticket._asdict())
    if request.method == 'PUT':
        new_status = request.json.get('status')
        ticket = TicketRepository.get_ticket(ticket_id)
        if not ticket:
            return Response(status=404)
        if new_status not in ticket_status_path[ticket.status]:
            return Response(status=400)
        TicketRepository.change_status(ticket_id, new_status)
        return Response(status=200)


@app.route('/tickets/<int:ticket_id>/comments')
def ticket_comments(ticket_id):
    if request.method == 'POST':
        data = request.json
        ticket = TicketRepository.get_ticket(ticket_id)
        if not ticket:
            return Response(status=404)
        Comment = namedtuple('Comment', ('email', 'text'))
        comment = Comment(data.get('email'), data.get('text'))
        TicketRepository.add_comment(ticket_id, comment)

if __name__ == '__main__':
    app.run()
