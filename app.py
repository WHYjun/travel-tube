# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, session, request, render_template
from flask_cors import CORS
from flask_oauth import OAuth

from googleapiclient.discovery import build
import googlemaps

import os
import json
import argparse
import requests

TEMPLATE_PATH = os.path.join(os.path.dirname((os.path.abspath(__file__))), 'client/') # app.js or index.html
STATIC_PATH = os.path.join(os.path.dirname((os.path.abspath(__file__))), 'client/static') # static files

try: # for localhost
    AUTH_PATH = os.path.join(os.path.dirname((os.path.abspath(__file__))), 'auth.json')
    # Get API keys from auth.json
    with open(AUTH_PATH) as auth:
        AUTH = json.load(auth)

    # Flask Configuration
    SECRET_KEY = AUTH['FLASK']['SECRET_KEY']

    # Youtube
    YOUTUBE_API_KEY = AUTH['YOUTUBE']['API_KEY']
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    # Eventbrite
    EVENTBRITE_OAUTH = AUTH['EVENTBRITE']['OAUTH_TOKEN']
    EVENTBRITE_URI = "https://www.eventbriteapi.com/v3/"

    # Twitter 
    TWITTER_API_KEY = AUTH['TWITTER']['API_KEY']
    TWITTER_API_SECRET = AUTH['TWITTER']['API_SECRET']

    # Google Maps
    GOOGLE_MAP_API_KEY = AUTH['GOOGLE_MAP']['API_KEY']
    gmaps = googlemaps.Client(key=GOOGLE_MAP_API_KEY)
except: # for heroku app
    # Youtube
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_KEY')
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    # Flask Configuration
    SECRET_KEY = os.environ.get('FLASK_KEY')

    # Eventbrite
    EVENTBRITE_OAUTH = os.environ.get('EVENTBRITE_OAUTH')
    EVENTBRITE_URI = "https://www.eventbriteapi.com/v3/"

    # Twitter 
    TWITTER_API_KEY = os.environ.get('TWITTER_KEY')
    TWITTER_API_SECRET = os.environ.get('TWITTER_SECRET')

    # Google Maps
    GOOGLE_MAP_API_KEY = os.environ.get('GOOGLE_MAP_KEY')
    gmaps = googlemaps.Client(key=GOOGLE_MAP_API_KEY)

# OAuth
oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET
)

app = Flask(__name__,template_folder=STATIC_PATH)
app.secret_key = SECRET_KEY
CORS(app)

@app.route('/', methods=['GET'])
def hello():
    return render_template('hello.html')

# Twitter Oauth from https://pythonspot.com/login-to-flask-app-with-twitter/
@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')
 
@app.route('/index')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))
 
    access_token = access_token[0]
 
    return render_template('index.html')
 
@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))
 
 
@app.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))
 
 
@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
 
    access_token = resp['oauth_token']
    session['access_token'] = access_token
    session['screen_name'] = resp['screen_name']
 
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    return redirect(url_for('index'))

@app.route('/search_result', methods=['POST'])
def search_result():
    keyword = request.form.get('keyword')
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default=keyword)
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()
    videos = youtube_search(args)
    return json.dumps(videos)
    # Just for team assignment 3
    # message = []
    # for video in videos:
    #     message.append(video['title'])
    # return render_template('search_result.html', message = message)


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

def eventbrite_search():
    headers =  {
    'Authorization': "Bearer " + EVENTBRITE_OAUTH,
    'Cache-Control': "no-cache",
    }
    params = {'location.address': 'Boston'}
    res = requests.request("GET", EVENTBRITE_URI+"events/search", headers = headers, params = params)
    event = json.loads(res.text)
    # Need Pre-processing before sending json to front-end
    return event

def reverse_geocode(GeoCode):
    return gmaps.reverse_geocode(GeoCode)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()