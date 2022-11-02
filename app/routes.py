from app import app
from flask import render_template, redirect, url_for

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

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
    return "Hello, world!"

@app.route('/logout')
def logout():
    return "Hello, world!"

