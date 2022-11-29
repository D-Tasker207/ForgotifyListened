import spotipy
from datetime import timedelta, datetime
from app import app, db
from flask import render_template, redirect, url_for, session, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.spotify_service import example_get, get_user, get_new_user_data, create_user_links, update_user_data
from app.models import User, Song, Album, Artist, UserToArtist, UserToSong, UserToAlbum

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
    return render_template('myStuffArtists.html', User=User, UserToArtist=UserToArtist)


@app.route('/most_forgotten_artists')
@login_required
def mostforgottenartists():
    return render_template('mostForgottenArtists.html')


@app.route('/one_year_artists')
@login_required
def oneyearartists():
    return render_template('yearAgoArtists.html')


@app.route('/six_months_artists')
@login_required
def sixmonthsartists():
    return render_template('sixMonthsArtists.html')


@app.route('/mystuff/songs')
@login_required
def mystuffsongs():
    return render_template('myStuffSongs.html', User=User, UserToSong=UserToSong)


@app.route('/most_forgotten_songs')
@login_required
def mostforgottensongs():
    return render_template('mostForgottenSongs.html')


@app.route('/one_year_songs')
@login_required
def oneyearsongs():
    return render_template('yearAgoSongs.html')


@app.route('/six_months_songs')
@login_required
def sixmonthssongs():
    return render_template('sixMonthsSongs.html')


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

@app.route('/new_user_dbpull')
def new_user_dbpull():
    # if(current_user.get_task_in_progress('create_user_links')):
    #     flash('Account scraping is in progress')
    # else:
    #     current_user.launch_task('create_user_links', "Gathering account info")
    #     db.session.commit()

    create_user_links()
    return redirect(url_for('mystuff/songs'))


@app.route('/testdbpull')
@login_required
def testdbpull():
    user_data = get_new_user_data()
    return user_data

