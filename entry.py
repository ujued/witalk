#!/usr/bin/env python3
import spmpool
from flup.server.fcgi import WSGIServer
from configuration import *
from flask import Flask, request, g, current_app, render_template, flash
from threading import current_thread
def create_app():
	spmpool.add_config('local', user=mysql_user, password=mysql_pass, database=mysql_db, host=mysql_host, init_pool_size=20)
	app = Flask(__name__)
	app.secret_key = '\x90m\x12\x98\x0b\xf4\xb8\x17m\x9eJK\x9aB`\xfe=\xe0\x99\x81S\xda-g'
	app.permanent = True
	app.connections = {}
	app.connect = lambda:app.connections[current_thread()]
	app.connection_pool = spmpool.spmpool('local')
	app.transactional = transactional
	################ remove soon #################
	class engine():
		def connect(self):
			return current_app.connection_pool.get()
	mysql_engine = engine()
	app.mysql_engine = mysql_engine
	##############################################
	# filters
	import markdown2
	from tools import get_date_fashion, get_post_device, support_at
	app.jinja_env.filters['fashion_date'] = get_date_fashion
	app.jinja_env.filters['post_device'] = get_post_device
	app.jinja_env.filters['support_at'] = support_at
	app.jinja_env.filters['markdown'] = markdown2.markdown
	# blueprints
	from witalk import bp as witalk_bp
	from passport import bp as passport_bp
	from nav import bp as nav_bp
	from message import bp as message_bp
	from collection import bp as collections_bp
	from search import bp as search_bp
	from pay import bp as pay_bp
	app.register_blueprint(witalk_bp)
	app.register_blueprint(passport_bp)
	app.register_blueprint(nav_bp)
	app.register_blueprint(message_bp)
	app.register_blueprint(collections_bp)
	app.register_blueprint(search_bp)
	app.register_blueprint(pay_bp)
	# template_global
	from services import svc_user, svc_message, svc_system
	app.add_template_global(svc_message.msgcount, 'msgcount')
	app.add_template_global(svc_system.currency, 'currency')
	app.add_template_global(svc_user.collectforums, 'collectforums')
	app.add_template_global(svc_user.interestedtopics, 'interestedtopics')
	app.add_template_global(svc_user.richusers, 'richusers')
	app.add_template_global(svc_user.points, 'points')
	app.add_template_global(svc_user.signined, 'signined')
	app.add_template_global(svc_user.signin, 'signin')
	return app

def plugin_run(app):
	from plugin import recent, onlines
	onlines.init(app)()
	recent.init(app)()

def transactional(func):
	def t_wrapper(*args):
		conn = current_app.connect()
		conn.begin()
		try:
			result = func(*args)
			conn.commit()
		except Exception as e:
			conn.rollback()
			flash(e)
			return render_template('404.html'), 404
		return result
	return t_wrapper

app = create_app()
plugin_run(app)

@app.before_request
def before_request(): # open connection
	app.connections[current_thread()] = app.connection_pool.get()
	mobile_list = ['Android', 'iPhone']
	for mobile in mobile_list:
		if mobile in request.headers.get('User-Agent'):
			g.tperfix = ''
			break
	if not hasattr(g, 'tperfix'):
		g.tperfix = 'pc/'

@app.after_request
def after_request(resp): # close connection
	ct = current_thread()
	if ct in app.connections:
		app.connections[ct].close()

	return resp

if __name__ == '__main__':
 	WSGIServer(app).run()
