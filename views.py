from collections import namedtuple

from flask import request, Response, jsonify
from flask.views import MethodView

from models import TicketRepository, WrongStatusException, Ticket


class TicketView(MethodView):
    def get(self, ticket_id):
        ticket = TicketRepository.get_ticket(ticket_id)
        if not ticket:
            return Response(status=404)
        return jsonify(ticket._asdict())

    def post(self):
        data = request.json
        ticket = Ticket(data.get('subject'), data.get('text'), data.get('email'))
        try:
            TicketRepository.create(ticket)
        except WrongStatusException:
            return Response(status=400)
        return Response(status=200)

    def put(self, ticket_id):
        new_status = request.json.get('status')
        ticket = TicketRepository.get_ticket(ticket_id)
        if not ticket:
            return Response(status=404)
        TicketRepository.change_status(ticket_id, new_status)
        return Response(status=200)


class CommentView(MethodView):
    def post(self, ticket_id):
        data = request.json
        ticket = TicketRepository.get_ticket(ticket_id)
        if not ticket:
            return Response(status=404)
        Comment = namedtuple('Comment', ('email', 'text'))
        comment = Comment(data.get('email'), data.get('text'))
        TicketRepository.add_comment(ticket_id, comment)
        return Response(status=200)
