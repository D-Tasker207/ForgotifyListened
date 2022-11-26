import spotipy
from datetime import timedelta, datetime
from app import app, db
from flask import render_template, redirect, url_for, session, request
from flask_login import current_user, login_user, logout_user, login_required
from app.spotify_service import example_get, get_user, get_new_user_data
from app.models import User, Song, Album, Artist, UserToArtist, UserToSong, UserToAlbum
from app.spotify_service import example_get, get_user, get_new_user_data, create_user_links, update_user_data

SCOPE = "user-top-read user-read-email playlist-modify-public"

# #function to call the data refresh functions when 90 days have passed since last pull
# @app.before_request
# def before_request():
#     if(current_user.is_authenticated):
#         today = datetime.today()
#         if User.query.filter_by(id=current_user.get_id()).first().last_pulled < today - timedelta(days=90):
#             redirect('/update_user_data')



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
    a_name = Artist.query.filter_by(name=name).first()
    return render_template('artist.html', artist=Artist, name=name)
    # return "Hello, %s!" % name


@app.route('/artistlist')
def artistlist():
    return "Hello, world!"


@app.route('/song/<name>')
def song(name):
    a_song = Song.query.filter_by(name=name).first()
    return render_template('song.html', song=Song, name=name)
    #return "Hello, %s!" % name


@app.route('/songlist')
def songlist():
    return "Hello, world!"


@app.route('/album/<name>')
def album(name):
    a_song = Album.query.filter_by(name=name).first()
    return render_template('album.html', album=Album, name=name)
    # return "Hello, %s!" % name


@app.route('/mystuff/artists')
@login_required
def mystuffartists():
    return render_template('myStuffArtists.html', User=User, UserToArtist=UserToArtist)


@app.route('/most_forgotten_artists')
@login_required
def mostforgottenartists():
    return render_template('mostForgottenArtists.html', User=User)


@app.route('/one_year_artists')
@login_required
def oneyearartists():
    return render_template('yearAgoArtists.html', User=User)


@app.route('/six_months_artists')
@login_required
def sixmonthsartists():
    return render_template('sixMonthsArtists.html', User=User)


@app.route('/mystuff/songs')
@login_required
def mystuffsongs():
    forgotten = []
    forgotten_img = []
    long_term = []
    long_term_img = []
    med_term = []
    med_term_img = []
    u = User.query.filter_by(id=current_user.id).first()
    song_ids = [x.song_id for x in u.songs]
    album_ids = [x.album_id for x in u.albums]
    song_names = [Song.query.filter_by(id=x).first() for x in song_ids]
    images = [Album.query.filter_by(id=x).first() for x in album_ids]

    # print(album_ids)
    # print(images)

    for i in range(len(song_names)):
        u2s = UserToSong.query.filter_by(song_id=song_names[i].id).first()
        # u2a = UserToAlbum.query.filter_by(album_id=images[i].id).first()
        if u2s.forgotten > 0:
            forgotten.append(song_names[i])
            forgotten_img.append(images[i])
        elif u2s.long_term > 0:
            long_term.append(song_names[i])
            long_term_img.append(images[i])

        else:
            med_term.append(song_names[i])
            med_term_img.append(images[i])

    # print(forgotten_img)
    # print(long_term_img)
    # print(med_term_img)
    # print(song_names)

    # if len(forgotten) == 0:
    # elif len(long_term) == 0 :
    # elif len(med_term) == 0:

    return render_template('myStuffSongs.html', User=User, forgotten=forgotten, long_term=long_term, med_term=med_term,
                           forgotten_img=forgotten_img, long_term_img=long_term_img, med_term_img=med_term_img)


@app.route('/most_forgotten_songs')
@login_required
def mostforgottensongs():
    return render_template('mostForgottenSongs.html', User=User)


@app.route('/one_year_songs')
@login_required
def oneyearsongs():
    return render_template('yearAgoSongs.html', User=User)


@app.route('/six_months_songs')
@login_required
def sixmonthssongs():
    return render_template('sixMonthsSongs.html', User=User)


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
    # print(get_user())
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
    user_data = get_new_user_data()
    create_user_links(user_data)
    return redirect(url_for('index'))

@app.route('/testdbpull')
@login_required
def testdbpull():
    user_data = get_new_user_data()
    return user_data

