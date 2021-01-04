"""
Run Flask API
"""
from app import app
import os

if __name__ == '__main__':

    # Debug based on environment
    if os.getenv('ENVIRONMENT') == 'PROD':
        app.run(debug=False)
    else:
        app.run(debug=True)