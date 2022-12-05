import spotipy
from datetime import timedelta, datetime
from app import app, db
from flask import render_template, redirect, url_for, session, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Song, Album, Artist, UserToSongF
from app.spotify_service import get_user, get_new_user_data, create_user_links, update_data

SCOPE = "user-top-read user-read-email"

#function to call the data refresh functions when 90 days have passed since last pull
@app.before_request
def before_request():
    if(current_user.is_authenticated):
        today = datetime.today()
        user = User.query.filter_by(id=current_user.get_id()).first()
        if user.last_pulled < today - timedelta(days=90):
            redirect('update_user_data')


@app.route('/')
@app.route('/index')
def index():
    mfs = UserToSongF.query.all()
    return render_template('index.html', mfs=mfs, title="Home")

@app.route('/artist/<id>')
def artist(id):
    artist = Artist.query.filter_by(id=id).first()
    return render_template('artist.html', artist=artist)

@app.route('/song/<id>')
def song(id):
    song = Song.query.filter_by(id=id).first()
    return render_template('song.html', song=song, title=song.name)

@app.route('/album/<id>')
def album(id):
    album = Album.query.first()
    return render_template('album.html', album=album, title=album.name)

@app.route('/mystuff/artists')
@login_required
def mystuffartists():
    u = User.query.filter_by(id=current_user.id).first()
    return render_template('myStuffArtists.html', user=u, title="My Artists")

@app.route('/most_forgotten_artists')
@login_required
def mostforgottenartists():
    u = User.query.filter_by(id=current_user.id).first()
    return render_template('mostForgottenArtists.html', user=u, title="My Most Forgotten Artists:")

@app.route('/one_year_artists')
@login_required
def oneyearartists():
    u = User.query.filter_by(id=current_user.id).first()
    return render_template('yearAgoArtists.html', user=u, title="One Year Ago")

@app.route('/six_months_artists')
@login_required
def sixmonthsartists():
    u = User.query.filter_by(id=current_user.id).first()
    return render_template('sixMonthsArtists.html', user=u, title="Six Months Ago")

@app.route('/mystuff/songs')
@login_required
def mystuffsongs():
    u = User.query.filter_by(id=current_user.id).first()
    return render_template('myStuffSongs.html', user=u, title="My Songs")


@app.route('/most_forgotten_songs')
@login_required
def mostforgottensongs():
    u = User.query.filter_by(id=current_user.id).first()
    return render_template('mostForgottenSongs.html', user=u, title="My Most Forgotten Artists")

@app.route('/one_year_songs')
@login_required
def oneyearsongs():
    u = User.query.filter_by(id=current_user.id).first()
    return render_template('yearAgoSongs.html', user=u, title="One Year Ago")

@app.route('/six_months_songs')
@login_required
def sixmonthssongs():
    u = User.query.filter_by(id=current_user.id).first()
    return render_template('sixMonthsSongs.html', user=u, title="Six Months Ago")

@app.route('/recommended')
def recommended():
    songs = Song.query.order_by('rec_count').all()
    albums = Album.query.order_by('rec_count').all()
    artists = Artist.query.order_by('rec_count').all()
    return render_template('recommended.html', songs=songs, albums=albums, artists=artists, title="Recommended")

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
    return redirect('/update_user_data')


@app.route('/logout')
@login_required
def logout():
    session.pop("token_info", None)
    logout_user()
    return redirect(url_for("index"))

@app.route('/get_email')
def get_email():
    return get_user()

@app.route('/update_user_data')
def update_user_data():
    update_data()
    return redirect(url_for("index"))

