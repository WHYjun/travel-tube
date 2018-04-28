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
 
    return redirect('http://localhost:3000/Tour')
 
@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized'))
 
 
@app.route('/logout')
def logout():
    session.pop('aceess_token', None)
    return redirect('http://localhost:3000/')
 
 
@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    if resp is None:
        return redirect('http://localhost:3000/')
 
    access_token = resp['oauth_token']
    session['access_token'] = access_token
    session['screen_name'] = resp['screen_name']
 
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    return redirect("http://localhost:3000/Tour")

@app.route('/search_result', methods=['POST'])
def search_result():
    latlng = json.loads(request.data)
    geocode = (latlng['lat'],latlng['lng'])
    events = eventbrite_search(latlng['lat'],latlng['lng'])
    address = reverse_geocode(geocode)
    city_name = get_cityname(address[0]['address_components'])
    keyword = city_name + 'tourism'
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default=keyword)
    parser.add_argument('--max-results', help='Max results', default=10)
    args = parser.parse_args()
    videos = youtube_search(args)
    data = {
        "city_name": city_name,
        "events": events,
        "videos": videos
    }
    return json.dumps(data)
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

    videos = {}
    index = 0

    # Store the result as a json format.
    for result in response.get('items', []):
        if result['id']['kind'] == 'youtube#video':
            key = "video" + str(index)
            index += 1
            videos[key] = {
                'title': result['snippet']['title'],
                'image_url': result['snippet']['thumbnails']['default'], # medium, high
                'channel_name': result['snippet']['channelTitle'],
                'video_id': result['id']['videoId']
            }
    return videos

def eventbrite_search(latitude, longitude):
    headers =  {
    'Authorization': "Bearer " + EVENTBRITE_OAUTH,
    'Cache-Control': "no-cache",
    }
    params = {'location.latitude': latitude, 'location.longitude': longitude}
    res = requests.request("GET", EVENTBRITE_URI+"events/search", headers = headers, params = params)
    event_dict = json.loads(res.text)
    events = {}
    index = 0
    for event in event_dict['events']:
        key = "event" + str(index)
        index += 1
        if index > 5:
            return events
        events[key] = {
            'name': event['name']['text'],
            'description': event['description']['text'],
            'url': event['url'],
            'start': event['start']['utc'],
            'end': event['end']['utc'],
            'id': event['id']
        }
        if event['logo'] is not None:
            events[key]['image_url'] = event['logo']['url']
    return events

def reverse_geocode(GeoCode):
    return gmaps.reverse_geocode(GeoCode)

def get_cityname(address_components):
    for component in address_components:
        if "locality" in component['types']:
            return component['short_name'] 

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()