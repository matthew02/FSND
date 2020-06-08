"""Decorators for API resources."""
import functools

from flask import request

from api.exception import BadRequestException


def expect_required_fields(func):
    """Examines an HTTP request to verify thit it contains all required fields.

    Raises:
        BadRequestException: If any any required fields are missing.
    """
    @functools.wraps(func)
    def decorated(instance, *args, **kwargs):
        request_data = request.get_json(force=True, silent=True)
        missing_fields = []
        given_fields = request_data.keys()
        for required_field in instance.__model__.required_fields():
            if required_field not in given_fields:
                missing_fields.append(required_field)
        if len(missing_fields) > 0:
            message = f'Missing required fields: [{", ".join(missing_fields)}]'
            raise BadRequestException(message)
        return func(instance, *args, **kwargs)
    return decorated

def refuse_unknown_fields(func):
    """Examines an HTTP request to verify thit it does not contain any
    unknown fields.

    Raises:
        BadRequestException: If any any unknown fields are discovered.
    """
    @functools.wraps(func)
    def decorated(instance, *args, **kwargs):
        request_data = request.get_json(force=True, silent=True)
        model = instance.__model__
        unknown_fields = []
        known_fields = model.required_fields() + model.optional_fields() + ['id']
        for given_field in request_data:
            if given_field not in known_fields:
                unknown_fields.append(given_field)
        if len(unknown_fields) > 0:
            message = f'Unknown fields: [{", ".join(unknown_fields)}]'
            raise BadRequestException(message)
        return func(instance, *args, **kwargs)
    return decorated

#def audit_request(func):
#    """Ensures that we have a valid request from the client.
#
#    Raises:
#        BadRequestException: If no data was received with the request.
#    """
#    @functools.wraps(func)
#    def decorated(instance, *args, **kwargs):
#        request_data = request.get_json(force=True, silent=True)
#        if not request_data:
#            raise BadRequestException('No data received with the request.')
