from flask import Blueprint, request, render_template, redirect, session, current_app, make_response
bp = Blueprint('nav', __name__)

@bp.route('/privacy')
def privacy():
	return render_template('privacy.html')

@bp.route('/about')
def about():
	return render_template('about.html')

@bp.route('/onlines')
def onlines():
	return render_template('onlines.html')

@bp.route('/forums')
def forums():
	conn = current_app.mysql_engine.connect()
	forum_count = conn.execute('select count(id) from forum').first()[0]
	conn.close()
	return render_template('forums.html', forum_count = forum_count)