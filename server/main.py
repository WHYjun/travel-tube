# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, session, request, render_template
from flask_cors import CORS
# from flask_oauth import OAuth

from googleapiclient.discovery import build

import os
import json
import argparse

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'client/') # app.js or index.html
STATIC_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'client/static') # static files
AUTH_PATH = os.path.join(os.path.dirname((os.path.abspath(__file__))), 'auth.json')

with open(AUTH_PATH) as auth:
    AUTH = json.load(auth)

YOUTUBE_API_KEY = AUTH['YOUTUBE']['API_KEY']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

app = Flask(__name__,template_folder=STATIC_PATH)
CORS(app)

@app.route('/', methods=['GET'])
def hello():
    return render_template('hello.html')

@app.route('/search_result', methods=['POST'])
def search_result():
    keyword = request.form.get('keyword')
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default=keyword)
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()
    videos = youtube_search(args)
    return json.dumps(videos)

# youtube search function
# Adapted from Youtube Sample Code: https://github.com/youtube/api-samples/blob/master/python/search.py
def youtube_search(options):
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=YOUTUBE_API_KEY
    )
    
    # Retrieve results from Youtube
    response = youtube.search().list(
        q=options.q,
        part='id,snippet',
        maxResults=options.max_results
    ).execute()

    videos = []

    # Store the result as a json format.
    for result in response.get('items', []):
        if result['id']['kind'] == 'youtube#video':
            videos.append({
                'title': result['snippet']['title'],
                'id': result['id']['videoId']
            })
    return videos


if __name__ == '__main__':
    app.run(debug=True)