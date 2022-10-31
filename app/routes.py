from app import app

@app.route('/')
@app.route('/home')
def index():
    return "Hello, world!"

@app.route('/artist/<name>')
def artist(name):
    return "Hello, %s!" % name

@app.route('/artistlist')
def artistlist():
    return "Hello, world!"

app.route('/song/<name>')
def song(name):
    return "Hello, %s!" % name

app.route('/songlist')
def songlist():
    return "Hello, world!"

app.route('album/<name>')
def album(name):
    return "Hello, %s!" % name

app.route('/mystuff/artists')
def mystuff():
    return "Hello, world!"

app.route*('/mystuff/songs')
def songs():
    return "Hello, world!"

app.route('recommended')
def recommended():
    return "Hello, world!"

app.route('contact')
def contact():
    return "Hello, world!"


@app.route('login')
def login():
    return "Hello, world!"

