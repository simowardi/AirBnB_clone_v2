#!/usr/bin/python3
"""Starts a Flask web application
    The application listens on 0.0.0.0, port 5000.
    Routes:
    /: Displays 'Hello HBNB!'
"""

from flask import Flask

# Create an instance of the Flask class for the web application.
app = Flask(__name__)
'''The Flask application instance.'''

# Disable strict slashes, so routes will work with or without a trailing slash.
app.url_map.strict_slashes = False

@app.route('/')
def index():
    '''The home page route.

    Returns:
        str: The greeting message "Hello HBNB!".
    '''
    return 'Hello HBNB!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
