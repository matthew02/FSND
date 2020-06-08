"""API interface for books."""
#from typing import Optional, Tuple

from flask import abort, request
#from flask import abort, jsonify, request
#from flask.views import MethodView
from sqlalchemy import exists
#from sqlalchemy import exc, exists


#from api.app import app
from api.exception import BadRequestException
from api.models.author import Author
from api.models.book import Book
from api.models.model import DB
from api.resources.resource import Service, register_api_all


class BookAPI(Service):
    """Class representing the book interface into the API."""
    def patch(self, resource_id: int) -> str:
        """Partially modifies a book in the database."""
        if 'author_id' in request.json:
            self.validate_author_id(request.json)
        return super().patch(resource_id)

    def post(self) -> str:
        """Adds a new book to the database."""
        self.validate_author_id(request.json)
        return super().post()

    def put(self, resource_id: int) -> str:
        """Replaces an existing book in the database."""
        self.validate_author_id(request.json)
        return super().put(resource_id)

    @staticmethod
    def validate_author_id(json: str) -> None:
        """Checks if the author exists in the database."""
        field = 'author_id'
        if (
               field not in json or
               not DB.session.query(
                   exists().where(
                       Author.id == json[field]
                   )).scalar()
        ):
            raise BadRequestException('Author not found.')

register_api_all(view=BookAPI, endpoint='book_api', model=Book, url='/books/')
