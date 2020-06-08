"""API interface for authors."""
import datetime

from flask import request

from api.models.author import Author
from api.exception import BadRequestException
from api.resources.resource import Service, register_api_all


class AuthorAPI(Service):
    """Class representing the author interface into the API."""

    def post(self):
        """Adds a new author to the database."""
        if request.json is None:
            raise Exception("AuthorAPI: No json in POST.")
        if 'birthdate' in request.json:
            try:
                request.json['birthdate'] = datetime.date.fromisoformat(
                    request.json.get('birthdate')
                )
            except (ValueError, TypeError):
                raise BadRequestException("AuthorAPI: Invalid date format.")
        return super().post()

register_api_all(view=AuthorAPI, endpoint='author_api', model=Author, url='/authors/')


#@app.route('/authors/<int:id>/books')
#def list_books_by_author(id):
#    return jsonify([
#        book.json()
#        for book
#        in Book.query.filter_by(author_id=id).all()
#    ])
