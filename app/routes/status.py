"""
Check server status.

"""
from flask import Blueprint, jsonify, request
from flask_api import status

status_bp = Blueprint(
    "status_bp",
    __name__,
    template_folder="routes"
)


@status_bp.route('/api/1/server_status', methods=['GET'])
def get_server_status():
    """ Get server status.

    Example:
        r = requests.get(
            'http://127.0.0.1:5000/api/1/server_status'
        )
        print(r.status_code)
        print(r.json())

    :return:
    """
    if request.method == 'GET':
        return jsonify({'status': 'ONLINE'}), status.HTTP_200_OK
