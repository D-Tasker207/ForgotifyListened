import spotipy
from app import app
from spotipy.oauth2 import SpotifyOAuth
from flask import render_template, redirect, url_for, session, request

from app.spotify_service import example_get

scope = "user-top-read user-read-email playlist-modify-public"

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/spotipytest')
def spotipytest():
    return example_get() #render_template('spotipy_test.html', songs=example_get())

@app.route('/artist/<name>')
def artist(name):
    return "Hello, %s!" % name

@app.route('/artistlist')
def artistlist():
    return "Hello, world!"

@app.route('/song/<name>')
def song(name):
    return "Hello, %s!" % name

@app.route('/songlist')
def songlist():
    return "Hello, world!"

@app.route('/album/<name>')
def album(name):
    return "Hello, %s!" % name

@app.route('/mystuff/artists')
def mystuff():
    return "Hello, world!"

@app.route('/mystuff/songs')
def songs():
    return "Hello, world!"

@app.route('/recommended')
def recommended():
    return "Hello, world!"

@app.route('/contact')
def contact():
    return "Hello, world!"

@app.route('/login')
def login():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    auth_url = auth_manager.get_authorize_url()
    return f'<h2><a href="{auth_url}">Sign in</a></h2>'

@app.route('/callback')
def callback():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    auth_manager.get_access_token(request.args.get("code"))
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop("token_info", None)
    return redirect(url_for("index"))