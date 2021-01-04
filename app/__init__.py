"""

"""
from flask_session import Session
from flask_api import FlaskAPI, status
from flask_assets import Environment
from flask_cors import CORS
from flask import jsonify
import logging
from .routes.status import status_bp

app = FlaskAPI(__name__)
app.logger.setLevel(logging.INFO)
CORS(app, resources=r'/api/*', supports_credentials=True)
app.config.from_object('config')
Environment(app)
Session(app)

app.register_blueprint(status_bp)


# Generic error handling
@app.errorhandler(400)
def bad_request(_):
    return jsonify({'error': 'Bad request'}), status.HTTP_400_BAD_REQUEST

@app.errorhandler(404)
def bad_request(_):
    return jsonify({'error': 'Not found'}), status.HTTP_404_NOT_FOUND

@app.errorhandler(405)
def bad_request(_):
    return jsonify({'error': 'Method not allowed'}), status.HTTP_405_METHOD_NOT_ALLOWED