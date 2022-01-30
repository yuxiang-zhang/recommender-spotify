from flask import Flask, redirect, request, jsonify, session, render_template, url_for
from flask_bootstrap import Bootstrap
from SpotifyApi import SpotifyApi
from RecommendStrat import MeanRS
from dotenv import load_dotenv

import os

from collections import Counter
from datetime import datetime, timedelta
import pytz

import pandas as pd

load_dotenv(".flaskenv")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
spotify = SpotifyApi(CLIENT_ID, CLIENT_SECRET)
login_callback_uri = "http://localhost:5000/callback"

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
bootstrap = Bootstrap(app)

strats = {'mean': MeanRS()}


@app.route("/")
def home():
    if 'expire_time' not in session or session['expire_time'] < datetime.now(pytz.UTC):
        session.clear()
        return render_template('index.html')
    return redirect('/me/playlists')
    return '<br/>'.join(('<a href=\'/me/playlists\'> My Playlists </a>',
                         '<a href=\'/recommend\'> My Recommendations </a>',
                         '<a href=\'/playlists/7DyH8C8HXh5RzYKKEy2BQI\'> Get Recommendations for Sample Playlist </a>',
                         '<a href=\'/logout\'> Logout </a>'))


@app.route("/login")
def hello():
    return redirect(spotify.build_auth_url(login_callback_uri))


@app.route('/logout')
def bye():
    session.clear()
    return redirect('/')


@app.route("/callback")
def init_session():

    try:
        token_json = spotify.get_access_token_json(
            request.args.get("code", ""), login_callback_uri
        )

        session.update(token_json)
        session['expire_time'] = datetime.now(pytz.UTC
                                              ) + timedelta(seconds=session['expires_in'])

        spotify.token_type = session['token_type']
        spotify.access_token = session['access_token']

        return redirect('/')

    except Exception as e:
        return str(e)


@app.route("/me/playlists")
def retrieve_playlists():
    try:
        playlists = spotify.get_my_playlists()['items']
        return render_template('inputplaylist.html', playlists=playlists)
    except:
        return bye()


@app.route("/playlists/<playlist_id>")
def retrieve_playlist_by_id(playlist_id):

    playlist = spotify.get_playlist_by_id(playlist_id)

    tracks = playlist['tracks']['items']
    session['track_ids'] = ','.join(track['track']['id'] for track in tracks)
    artist_ids = Counter(
        artist['id'] for track in tracks for artist in track['track']['artists'])
    session['artist_ids'] = ','.join(
        artist_id for artist_id, _ in artist_ids.most_common(5))
    return redirect('/recommend')


@app.route('/recommend')
def select_strategy():
    if 'track_ids' in session:
        return '<br/>'.join(('<a href=\'/recommend/mean\' style=\"border-radius: 8pt; border-style:inset; border-color:#984B43; background:#D7CEC7;right: 25px;top: 15px\"> Simple Recommendation </a>',))
    return redirect('/')


@app.route("/recommend/<strat_name>")
def recommend(strat_name):
    try:
        strat = strats.get(strat_name, MeanRS())

        track_ids = session.get('track_ids', '')
        track_features = pd.json_normalize(
            spotify.get_tracks_features(track_ids))

        artist_ids = session.get('artist_ids', '')
        recommended_tracks = spotify.get_recommendations(
            strat.recommend(track_features, artist_ids))['tracks']
        return render_template('outputplaylist.html', tracks=recommended_tracks)
    except Exception as e:
        return bye()
