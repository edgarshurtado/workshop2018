from app import app, db
from flask import render_template


@app.errorhandler(404)
def not_found_error(error):
    # The second returned parameter is for avoiding the client to get a 200 status code
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
