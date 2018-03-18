#!/usr/bin/env python3
import json, markdown2, datetime, time, redis, os
from flup.server.fcgi import WSGIServer
from queue import Queue
from threading import Thread
from config import configuration as conf
from flask import Flask, session, request, g
from sqlalchemy import create_engine
from tools import get_date_fashion, get_post_device, support_at, update_online_users, create_recent_topic_item, update_online_users
from witalk import create_topic_item

engine = create_engine('mysql+pymysql://%(mysql_user)s:%(mysql_pass)s@127.0.0.1/%(mysql_db)s?charset=utf8' % conf)
r = redis.Redis(host=conf['redis_host'], password=conf['redis_pass'])

def create_app():
    app = Flask(__name__)
    return app

app = create_app()
app.secret_key = '\x90m\x12\x98\x0b\xf4\xb8\x17m\x9eJK\x9aB`\xfe=\xe0\x99\x81S\xda-g'
app.permanent = True

# about online user
online_usernames = []
online_users = []
online_user_updates_queue = Queue()
app.online_usernames = online_usernames
app.online_users = online_users
app.online_user_updates_queue = online_user_updates_queue
def update_oluser_date():
	while True:
		name = online_user_updates_queue.get()
		for user in online_users :
			if user['name'] == name:
				user['last_time'] = datetime.datetime.now()
def update_online_user():
	while True:
		time.sleep(300)
		max_online_count = r.get('max_online_count');
		now_count = len(online_users)
		if not max_online_count or int(max_online_count) < now_count:
			r.set('max_online_count', now_count)
		for user in online_users:
			if (datetime.datetime.now() - user['last_time']).seconds > 180:
				online_users.remove(user)
				online_usernames.remove(user['name'])
Thread(target=update_oluser_date).start()
Thread(target=update_online_user).start()
@app.template_global('onlines')
def onlines():
	return online_users
@app.template_global('max_online_count')
def max_online_count():
	max_online_count = r.get('max_online_count')
	if not max_online_count:
		max_online_count = 1
	return int(max_online_count)

# abount recent topics
programming_forum_ids = '2,3,4,5,6,7,8,9,10,11,12,13,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,35,39,40,41'
art_forum_ids = '33,34,38'
trade_forum_ids = '14,15'
app.programming_forum_ids = programming_forum_ids
app.art_forum_ids = art_forum_ids
app.trade_forum_ids = trade_forum_ids
def on_first_run():
	app.all_recent_topic_ids = []
	app.programming_recent_topic_ids = []
	app.art_recent_topic_ids= []
	app.trade_recent_topic_ids = []
	conn = engine.connect()
	all_row = conn.execute('select id from topic order by post_date desc limit 24').fetchall()
	programming_row = conn.execute('select id from topic where forum_id in (%s) order by post_date desc limit 24' % programming_forum_ids).fetchall()
	art_row = conn.execute('select id from topic where forum_id in (%s) order by post_date desc limit 24' % art_forum_ids).fetchall()
	trade_row = conn.execute('select id from topic where forum_id in(%s) order by post_date desc limit 24' % trade_forum_ids).fetchall()
	for t1 in all_row:
		app.all_recent_topic_ids.append(t1.id)
	for t2 in programming_row:
		app.programming_recent_topic_ids.append(t2.id)
	for t3 in art_row:
		app.art_recent_topic_ids.append(t3.id)
	for t4 in trade_row:
		app.trade_recent_topic_ids.append(t4.id)
	conn.close()
if r.get('all_recent_topic_ids') is None:
	on_first_run()
else:
	app.all_recent_topic_ids = eval(r.get('all_recent_topic_ids'))
	app.programming_recent_topic_ids = eval(r.get('programming_recent_topic_ids'))
	app.art_recent_topic_ids = eval(r.get('art_recent_topic_ids'))
	app.trade_recent_topic_ids = eval(r.get('trade_recent_topic_ids'))
def save_recent_topics():
	while True:
		time.sleep(60)
		r.set('all_recent_topic_ids', app.all_recent_topic_ids)
		r.set('programming_recent_topic_ids', app.programming_recent_topic_ids)
		r.set('art_recent_topic_ids', app.art_recent_topic_ids)
		r.set('trade_recent_topic_ids', app.trade_recent_topic_ids)
Thread(target=save_recent_topics).start()

app.jinja_env.filters['fashion_date'] = get_date_fashion
app.jinja_env.filters['post_device'] = get_post_device
app.jinja_env.filters['support_at'] = support_at
app.jinja_env.filters['markdown'] = markdown2.markdown
app.mysql_engine = engine

from witalk import bp as witalk_bp
from passport import bp as passport_bp
from nav import bp as nav_bp
from message import bp as message_bp
from collection import bp as collections_bp

app.register_blueprint(witalk_bp)
app.register_blueprint(passport_bp)
app.register_blueprint(nav_bp)
app.register_blueprint(message_bp)
app.register_blueprint(collections_bp)

@app.before_request
def update_onlines():
	if request.cookies.get(app.session_cookie_name) is None:
		request.username = str(os.urandom(32))
		update_online_users(session, app, request, request.username)
	else:
		update_online_users(session, app, request)

	mobile_list = ['Android', 'iPhone']
	for mobile in mobile_list:
		if mobile in request.headers.get('User-Agent'):
			g.tperfix = ''
			break
	if not hasattr(g, 'tperfix'):
		g.tperfix = 'pc/'

@app.after_request
def ensure_session(resp):
	if request.cookies.get(app.session_cookie_name) is None:
		resp.set_cookie(app.session_cookie_name, value = request.username)
	return resp

@app.template_global('msgcount')
def msgcount():
	if 'ol_user' in session:
		conn = engine.connect()
		count = conn.execute('select count(id) from message where to_id=%d and readed=0' % session['ol_user']['id']).first()[0]
		conn.close()
	else:
		count = -1
	return count
app.run(host='0.0.0.0')

# if __name__ == '__main__':
# 	WSGIServer(app).run()
