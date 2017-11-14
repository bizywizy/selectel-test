from views import TicketView, CommentView
from app import app

app.add_url_rule('/tickets/', view_func=TicketView.as_view('ticket_create'), methods=['POST'])
app.add_url_rule('/tickets/<int:ticket_id>', view_func=TicketView.as_view('ticket'),
                 methods=['GET', 'PUT', 'DELETE'])
app.add_url_rule('/tickets/<int:ticket_id>/comments', view_func=CommentView.as_view('comment_create'),
                 methods=['POST'])

if __name__ == '__main__':
    app.run()
