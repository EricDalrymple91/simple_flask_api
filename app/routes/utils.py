"""

"""
from flask import current_app, request, jsonify
from flask_api import status
from functools import wraps

def request_auth_wrapper(orig_func):
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get('X-Auth-Token', None)
        if auth_token == 'XYZ':
            return orig_func(*args, **kwargs)
        else:
            current_app.logger.error('Unauthorized')
            return jsonify({'error': 'Unauthorized'}), status.HTTP_401_UNAUTHORIZED

    return wrapper
