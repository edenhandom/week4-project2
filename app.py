
import os
import json
import openai
import requests
from openai import OpenAI

import re
from markupsafe import Markup
from flask import Flask, request, redirect, session, url_for, render_template, flash


from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)


# FOR SPOTIFY API
CLIENT_ID = 'ad91a46157df4ba080456f92c7a74ef8'
CLIENT_SECRET = '9d4140d511c64467a582b075b990cbfe'


redirect_uri = 'http://localhost:3000/callback'


# Look into this
sp_oauth = SpotifyOAuth(
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET,
  redirect_uri=redirect_uri,
  show_dialog=True
)

sp = Spotify(auth_manager=sp_oauth)

# FOR OPEN AI API
USER_KEY = 'sk-proj-1khMfBUfzzDLj5qcLf9GT3BlbkFJMUuRf6O2GEKGjNEfIqNk'
# Create an OpenAPI client
client = OpenAI(api_key=USER_KEY)


# Get response from Chat GPT
def get_chat_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": 
            ("You are a musical genius that's good at reading people.")},
            {"role": "user", "content": prompt}
            ]
    )
    message = response.choices[0].message.content
    return message



# Get track ID from a track name
def get_track_id(track_name):
    
    base_url = 'https://api.spotify.com/v1/search'
    searchResults = sp.search(q="track:" + track_name, type="track", limit=1)
    tracks = searchResults.get('tracks', {}).get('items', [])
    if tracks:
        return tracks[0]['id']
    else:
        return None


# Get a song link from a track ID
def get_song_link(track_id):
    # Base URL for Spotify track links
    base_url = 'https://open.spotify.com/track/'
    
    # Construct the full Spotify track link
    track_link = base_url + track_id
    
    return track_link

# Test code for above
print(get_track_id("Sha Sha Sha"))
id = get_track_id("Sha Sha Sha")
print(get_song_link(id))