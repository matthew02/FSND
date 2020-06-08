"""Base for API resources as HTTP endpoints."""

from typing import Optional, Type, TypeVar

from flask import current_app, jsonify, make_response, request
from flask.views import MethodView
from flask.wrappers import Response

#from api.app import app
from api.exception import BadRequestException
from api.models.model import db, Model
from api.resources.decorators import expect_required_fields, refuse_unknown_fields
from config import Config


M = TypeVar('M', bound='Model')
R = TypeVar('R', bound='Resource')

class Resource(MethodView):
    """Base class for HTTP endpoints."""

    __model__: Optional[M] = None

    def __init__(self, model: M) -> None:
        self.__model__ = model

    def delete(self, resource_id: int, *args, **kwargs) -> Response:
        """Deletes the specified resource."""
        resource = self.__model__.delete_by_id(resource_id)
        return self._no_content_response()

    def get(self, resource_id: Optional[int] = None) -> Response:
        """Fetches one or all resources from the database. If resource_id
        is given, return that specific resource, otherwise return all."""
        if resource_id is not None:
            resources = self.__model__.fetch_by_id(resource_id)
        elif 'page' in request.args:
            page = int(request.args.get('page'))
            resources = self.__model__.fetch_page(page, Config.PAGE_LENGTH)
        else:
            resources = self.__model__.fetch_all()

        return jsonify(resources)

    #@audit_request
    @refuse_unknown_fields
    def patch(self, resource_id: int) -> Response:
        """Applies partial modifications to the given resource.

        Raises: BadRequestException if the requested resource doesn't exist.
        """
        if not request.get_json():
            raise BadRequestException('No JSON data received.')
        resource = self.__model__.fetch_one(resource_id).json()
        resource.update(**request.get_json)
        return jsonify(resource)

    #@audit_request
    @expect_required_fields
    @refuse_unknown_fields
    def post(self) -> Response:
        """Creates a new resource.

        Raises: BadRequestException if the given resource doesn't match
        the model.
        """
        # Check for an existing resource matching this description
        if self.__model__.query.filter_by(**request.get_json()).first():
            return self._no_content_response()

        if 'id' in request.get_json:
            raise BadRequestException('Cannot specify id with POST request.')

        resource = self.__model__(**request.get_json)
        error_message = resource.validate_all(request.get_json)
        if error_message:
            raise BadRequestException(error_message)
        self.__model__.insert(resource)
        return self._created_response(resource.json())

    #@audit_request
    @expect_required_fields
    @refuse_unknown_fields
    def put(self, resource_id: int) -> Response:
        """Replaces the specified resource."""
        resource = self.__model__.fetch_one(resource_id).json()
        if 'id' in request.get_json and resource_id != request.get_json['id']:
            raise BadRequestException('Cannot change the id of an existing resource.')
        resource.update(**request.get_json)
        return jsonify(resource)

    @staticmethod
    def _created_response(resource: M) -> Response:
        """Returns an HTTP 201 (Created) response."""
        response = jsonify(resource)
        response.status_code = 201
        return response

    @staticmethod
    def _no_content_response() -> Response:
        """Returns an HTTP 204 (No Content) response."""
        response = make_response()
        response.status_code = 204
        return response

#def register_api_some(view, endpoint, model, url, pk='id', pk_type='int'):
#    """Registers an HTTP endpoint."""

def register_api_all(view: R,
                     endpoint: str,
                     model: M,
                     url: str,
                     pk:str = 'resource_id',
                     pk_type: str = 'int') -> None:
    """Registers an HTTP endpoint with all HTTP methods."""
    view_func = view.as_view(endpoint, model)


    current_app.add_url_rule(
        url,
        defaults={pk: None},
        view_func=view_func,
        methods=['GET']
    )

    current_app.add_url_rule(
        url,
        view_func=view_func,
        methods=['POST']
    )

    current_app.add_url_rule(
        f'{url}/<{pk_type}:{pk}>',
        view_func=view_func,
        methods=['DELETE', 'GET', 'PATCH']
        #methods=['DELETE', 'GET', 'PATCH', 'PUT']
    )
