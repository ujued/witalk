import os, time, datetime
from threading import Thread
from queue import Queue
from tools import update_online_users, update_online_users
from flask import request

def init(app):
	online_usernames = []
	online_users = []
	online_user_updates_queue = Queue()
	plugin_data = os.getcwd() + '/data/onlines.tdb'
	if not os.path.exists(plugin_data):
		with open(plugin_data, 'w+') as f:
			f.write('0')
		app.max_online_count = 0
	else:
		with open(plugin_data) as f:
			app.max_online_count = int(f.readline().strip())
	app.online_usernames = online_usernames
	app.online_users = online_users
	app.online_user_updates_queue = online_user_updates_queue

	@app.template_global('onlines')
	def onlines():
		return online_users
	@app.template_global('max_online_count')
	def max_online_count():
		return app.max_online_count
	@app.before_request
	def update_onlines():
		if request.cookies.get(app.session_cookie_name) is None:
			request.username = str(os.urandom(32))
		update_online_users()
	@app.after_request
	def ensure_session(resp):
		if request.cookies.get(app.session_cookie_name) is None:
			resp.set_cookie(app.session_cookie_name, value = request.username)
		return resp

	def update_oluser_date():
		while True:
			name = online_user_updates_queue.get()
			for user in online_users :
				if user['name'] == name:
					user['last_time'] = datetime.datetime.now()
	def update_online_user():
		while True:
			time.sleep(300)
			now_count = len(online_users)
			if app.max_online_count < now_count:
				with open(plugin_data, 'w+') as f:
					f.write(str(now_count))
				app.max_online_count = now_count
			for user in online_users:
				if (datetime.datetime.now() - user['last_time']).seconds > 180:
					online_users.remove(user)
					online_usernames.remove(user['name'])
	def run():
		Thread(target=update_oluser_date).start()
		Thread(target=update_online_user).start()
	return run