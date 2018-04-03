from flask import current_app, session
from threading import current_thread

def price(id):
	column(id, 'price')[0]
def column(column_name, id):
	conn = current_app.connections[current_thread()]
	c_row = conn.execute('select %s from topic where id=%d' % (column_name, id)).first()
	if c_row:
		return c_row
	else:
		return None