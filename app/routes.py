import spotipy
from datetime import timedelta, datetime
from app import app, db
from flask import render_template, redirect, url_for, session, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Song, Album, Artist
from app.spotify_service import get_user, get_new_user_data, create_user_links, update_user_data

SCOPE = "user-top-read user-read-email playlist-modify-public"

# #function to call the data refresh functions when 90 days have passed since last pull
# @app.before_request
# def before_request():
#     if(current_user.is_authenticated):
#         today = datetime.today()
#         user = User.query.filter_by(id=current_user.get_id()).first()
#         if user.last_pulled < today - timedelta(days=90):
#             redirect('update_user_data')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")

@app.route('/artist/<name>')
def artist(name):
    return render_template('artist.html', artist=Artist, name=name)

@app.route('/artistlist')
def artistlist():
    return "Hello, world!"

@app.route('/song/<name>')
def song(name):
    song_id = Song.query.filter_by(name=name).first()
    artist_id = [x.artist_id for x in song_id.artist2song]
    artist = [Artist.query.filter_by(id=x).first().name for x in artist_id]

    return render_template('song.html', Song=Song, name=name, artist=artist, size=len(artist))

@app.route('/songlist')
def songlist():
    return "Hello, world!"

@app.route('/album/<name>')
def album(name):
    return render_template('album.html', album=Album, name=name)

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
    return redirect('/new_user_dbpull')


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
    update_user_data()
    return redirect(url_for("index"))

@app.route('/new_user_dbpull')
def new_user_dbpull():
    create_user_links()
    return redirect(url_for('index'))

@app.route('/testdbpull')
@login_required
def testdbpull():
    user_data = get_new_user_data()
    return user_data

