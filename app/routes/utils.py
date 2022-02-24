"""

"""
from flask import current_app, request, jsonify
from flask_api import status
from functools import wraps


def request_wrapper(orig_func):
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        current_app.logger.info(f'{request.method} - {request.url} ({request.is_secure})')
        try:
            return orig_func(*args, **kwargs)
        except Exception as error:
            error_msg = f'{type(error).__name__}: {error}'
            current_app.logger.error(f'{error_msg}')
            current_app.logger.exception(error)

            if '404' in error_msg:
                return {'error': error_msg}, status.HTTP_404_NOT_FOUND
            else:
                return {'error': error_msg}, status.HTTP_500_INTERNAL_SERVER_ERROR

    return wrapper


def request_auth_wrapper(orig_func):
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        current_app.logger.info(f'{request.method} - {request.url} ({request.is_secure})')
        auth_token = request.headers.get('X-Auth-Token', None)
        if auth_token == 'XYZ':
            return orig_func(*args, **kwargs)
        else:
            current_app.logger.error('Unauthorized')
            return jsonify({'error': 'Unauthorized'}), status.HTTP_401_UNAUTHORIZED

    return wrapper
