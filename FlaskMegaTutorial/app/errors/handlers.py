from app import db
from flask import render_template
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    # The second returned parameter is for avoiding the client to get a 200 status code
    return render_template('404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
