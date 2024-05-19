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
app.url_map.strict_slashes = False

@app.route('/')
def index():
    """returns Hello HBNB!"""
    return 'Hello HBNB!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
