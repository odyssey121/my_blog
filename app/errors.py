from app import app, db
from flask import render_template


@app.errorhandler(404)
def not_found_error(error):
	return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('errors/500.html'), 500

@app.errorhandler(403)
def not_access(error):
	return render_template('errors/403.html'), 403