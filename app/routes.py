import spotipy
from app import app, db
from spotipy.oauth2 import SpotifyOAuth
from flask import render_template, redirect, url_for, session, request
from flask_login import current_user, login_user, logout_user, login_required
from app.spotify_service import example_get, get_user
from app.models import User, Song, Album, Artist

SCOPE = "user-top-read user-read-email playlist-modify-public"


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/spotipytest')
@login_required
def spotipytest():
    return render_template('spotipy_test.html', songs=example_get())


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
@login_required
def mystuffartists():
    return render_template('myStuffArtists.html')


@app.route('/mystuff/songs')
@login_required
def mystuffsongs():
    return render_template('myStuffSongs.html')


@app.route('/recommended')
def recommended():
    return render_template('recommended.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # form = ContactUsForm()
    # return render_template('contact.html', title='Contact Us', form=form)
    return "Hello, world!"


@app.route('/login')
def login():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=SCOPE,
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    auth_manager.get_access_token(request.args.get("code"))

    user = User.query.filter_by(email=get_user()['email']).first()

    if user is None:
        user = User(email=get_user()['email'])
        db.session.add(user)
        db.session.commit()

        login_user(user)
    else:
        login_user(user)
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop("token_info", None)
    logout_user()
    return redirect(url_for("index"))

@app.route('/get_email')
def get_email():
    return get_user()