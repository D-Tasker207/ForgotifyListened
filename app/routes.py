from app import app
from flask import render_template, redirect, url_for
# from app.forms import ContactUsForm
from app.spotify_service import Spotify


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/spotipytest')
def spotipytest():
    session = Spotify()
    return session.example_get()


@app.route('/callback')
def callback():
    return redirect(url_for('index'))


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
def mystuffartists():
    return render_template('myStuffArtists.html')


@app.route('/mystuff/songs')
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
    return "Hello, world!"


@app.route('/logout')
def logout():
    return "Hello, world!"

