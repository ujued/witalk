import hashlib
from flask import session, current_app
from threading import current_thread
from datetime import datetime

def points(uid=None):
	if not uid:
		if 'ol_user' in session:
			uid = session['ol_user']['id']
		else:
			return 0
	conn = current_app.connections[current_thread()]
	value = conn.execute('select points from user where id=%d' % uid).first()
	if value:
		return value[0]
	else:
		return 0
def check_password(password, uid=None):
	conn = current_app.connections[current_thread()]
	if not uid:
		if 'ol_user' in session:
			uid = session['ol_user']['id']
		else:
			return False
	password_row = conn.execute('select password from user where id=%d' % uid).first()
	password = hashlib.md5(password.encode('utf-8')).hexdigest()
	if password_row and password_row[0] == password:
		return True
	else:
		return False
def check_bag(goods_name, goods_id, uid=None):
	conn = current_app.connections[current_thread()]
	if not uid:
		if 'ol_user' in session:
			uid = session['ol_user']['id']
		else:
			return False
	count = conn.execute("select count(id) from bag where goods_name='%s' and goods_id=%d" % (goods_name, goods_id)).first()[0]
	if count == 1:
		return True
	return False
def richusers():
	conn = current_app.connections[current_thread()]
	return conn.execute("select * from (select id,name,avatar,points,gender from user order by register_date asc) as tmp order by points desc limit 10").fetchall()

def collectforums(uid=None): # own fav forums
	if not uid:
		if 'ol_user' in session:
			uid = session['ol_user']['id']
		else:
			return None
	conn = current_app.connections[current_thread()]
	return conn.execute("select id,name from forum where id in (select collect_id from collection where owner_id=%d and collect_cate='f')" % uid).fetchall()
def interestedtopics(): # from fav forums
	if 'ol_user' in session:
		conn = current_app.connections[current_thread()]
		return conn.execute("select topic.id id,title,view_count,author_id,user.avatar author_avatar, forum_id from topic left join user on topic.author_id = user.id where topic.forum_id in (select collect_id from collection where owner_id=%d and collect_cate='f') order by topic.post_date desc limit 10" % session['ol_user']['id']).fetchall()
	else:
		return None
def max_signin_days():
	if 'ol_user' not in session:
		return 0
	max_days = conn.execute('select max_days from signin_record where user_id=%d' % session['ol_user']['id']).first()
	if not max_days:
		return 0
	return max_days[0]

def signin():
	if 'ol_user' not in session:
		return -1
	uid = session['ol_user']['id']
	conn = current_app.connections[current_thread()]
	record = conn.execute('select * from signin_record where user_id=%d' % uid).first()
	nowd = datetime.now()
	nowdstr = nowd.strftime('%Y-%m-%d %H:%M:%S')
	if record:
		if nowd.date() == record.last_signin_date.date():
			return 0
		cz = nowd - record.last_signin_date
		if cz.seconds < 1440 * 60:
			if record.endless_days+1 > record.max_days:
				max_days = record.endless_days+1
			else:
				max_days = record.max_days
			conn.execute("update signin_record set endless_days=endless_days+1, last_signin_date='%s', max_days=%d where id=%d" % (nowdstr, max_days, record.id))
			update_points(+(4 + record.endless_days), trade_info = 'signin, %ddays' % (record.endless_days+1))
			return 4 + record.endless_days
		else:
			conn.execute("update signin_record set endless_days=1, last_signin_date='%s' where id=%d" % (nowdstr, record.id))
			update_points(+4, trade_info = 'signin')
			return 4
	else:
		conn.execute("insert into signin_record(user_id, endless_days, last_signin_date) values(%d, %d, '%s')" % (uid, 1, nowdstr))
		update_points(+4, trade_info = 'signin, first time')
		return 4
def signined():
	if 'ol_user' not in session:
		return False
	conn = current_app.connections[current_thread()]
	last_signin_date = conn.execute("select last_signin_date from signin_record where user_id=%d" % session['ol_user']['id']).first()
	if last_signin_date:
		if last_signin_date[0].date() == datetime.now().date():
			return True
	return False
def pack_bag(goods_name, goods_id, uid=None):
	conn = current_app.connections[current_thread()]
	if not uid:
		if 'ol_user' in session:
			uid = session['ol_user']['id']
		else:
			return
	conn.execute("insert into bag(goods_id, goods_name, user_id) values(%d, '%s', %d)" % (goods_id, goods_name, uid))
def update_points(points, uid=None, trade_info='unkonwn trade'):
	conn = current_app.connections[current_thread()]
	if not uid:
		if 'ol_user' in session:
			uid = session['ol_user']['id']
		else:
			return
	conn.execute('update user set points=points+%d where id=%d' %(points, uid))
	conn.execute("insert into bill (user_id, trade, trade_info) values(%d, %d, '%s')" % (uid, points, trade_info))