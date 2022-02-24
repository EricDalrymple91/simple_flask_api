"""
Mock data.

"""
from flask import Blueprint, jsonify, request
from flask_api import status
from .utils import request_auth_wrapper
import re

data_bp = Blueprint(
    "data_bp",
    __name__,
    template_folder="routes"
)

MOCK_DATA = {
    'A': 10,
    'B': [1, 2, 3],
    'C': {
        'c1': "C TEST A",
        'c2': 'C TEST B'
    },
    'D': 'D TEST',
    'E': ['E TEST A', 'E TEST B']
}


@data_bp.route('/api/1/data', methods=['GET'])
def get_data():
    """ Get mock data.

    Example:
        r = requests.get(
            'http://127.0.0.1:5000/api/1/data'
        )
        print(r.status_code)
        print(r.json())

    :return:
    """
    if request.method == 'GET':
        return jsonify({'data': MOCK_DATA}), status.HTTP_200_OK


@data_bp.route('/api/1/data/<key>', methods=['GET'])
def get_data_by_key(key):
    """ Get mock data by a key.

    Example:
        r = requests.get(
            'http://127.0.0.1:5000/api/1/data/A'
        )
        print(r.status_code)
        print(r.json())

    :param key:
    :return:
    """
    if request.method == 'GET':
        try:
            data = MOCK_DATA[key]
        except KeyError:
            return jsonify({'error': f'{key} does not exist in the dataset'}), status.HTTP_400_BAD_REQUEST

        return jsonify({'data': data}), status.HTTP_200_OK


@data_bp.route('/api/1/data', methods=['POST'])
@request_auth_wrapper
def add_data():
    """ Post more info to the mock data object (doesn't obviously change anything)

    Example:
        r = requests.post(
            'http://127.0.0.1:5000/api/1/data',
            json={'X': 5},
            headers={'X-Auth-Token': 'XYZ'}
        )
        print(r.status_code)
        print(r.json())

    :return:
    """
    if request.method == 'POST':
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({'error': 'Added data must be an object'}), status.HTTP_400_BAD_REQUEST

        for key in data.keys():
            if not re.match('[A-Z]', key):
                return jsonify({'error': f'{key} must be a capital letter'}), status.HTTP_400_BAD_REQUEST

        MOCK_DATA.update(data)

        return jsonify({'data': MOCK_DATA}), status.HTTP_200_OK


