# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, session, request
from flask_oauth import OAuth

import os
import json

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "client/") # app.js or index.html
STATIC_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "client/static") # static files
AUTH_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "auth.json")

app = Flask(__name__,static_folder=STATIC_PATH)

@app.route('/')
def hello():
    return 'hello\n'

if __name__ == '__main__':
    app.run(debug=True)

# TODO: Twitter OAuth
# Documentation: https://pythonhosted.org/Flask-OAuth/
# TODO: Spotify OAuth
# Documentation: https://beta.developer.spotify.com/documentation/web-api/reference/
# TODO: FitBit OAuth
# Documentation: https://dev.fitbit.com/build/reference/web-api/
# TODO: Generate the playlist from Spotify API with considering user's average speed(for bpm?)

# TODO: If available, get data from FitBit. If not, ask users to put average speed and distance.

# TODO: Use Google Map to generate the running course with user's average distance
