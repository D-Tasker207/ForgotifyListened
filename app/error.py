from app import app, db
from flask import render_template, url_for

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', title="Error 500"), 500