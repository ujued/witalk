from threading import current_thread
from flask import current_app, session

def msgcount(): # new message count
	if 'ol_user' in session:
		conn = current_app.connections[current_thread()]
		count = conn.execute('select count(id) from message where to_id=%d and readed=0' % session['ol_user']['id']).first()[0]
	else:
		count = -1
	return count