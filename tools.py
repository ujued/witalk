import datetime, hashlib, re
from flask import session
def filter_sql(list):
	for x in range(0,len(list)):
		list[x] = list[x].replace("'", "''").replace('%', '__bfh_')
	return list

def page_turning_info(item_count, current_page = 1, page_count = 12):
	pgs = int(item_count / page_count)
	opg = item_count % page_count
	limit = '0,1'
	if current_page <= 0 or item_count == 0:
		have = False
	else:
		have = True
		if current_page <= pgs:
			limit = '%d, %d' % (item_count - current_page * page_count, page_count)
		elif current_page is pgs + 1:
			limit = '0, %d' % opg
		else:
			have = False
	return {
		'pgs':pgs,
		'opg':opg,
		'have':have,
		'limit':limit
	}

def get_date_fashion(dt):
	cz  = datetime.datetime.now() - dt
	if cz.days > 0:
		mounths = cz.days/30
		if mounths >=1:
			return '%d月' % int(mounths)
		return '%d天' % cz.days
	else:
		secs = cz.seconds
		minutes = secs/60
		hours = minutes/60
		if hours >=1 :
			return '%d小时' % int(hours)
		elif minutes >= 1:
			return '%d分钟' % int(minutes)
		return '%d秒' % int(secs)

def get_post_device(user_agent):
	if user_agent is None:
		return None
	device = user_agent.split(')')[0].split('; ')[-1]
	konwns_rel_devices = ['Letv X500', 'vivo X9', 'PRA-AL00X', 'Linux', 'iPhone OS', 'google.com', 'baidu.com']
	konwns_devices = ['Le 1s', 'vivo X9', '荣耀8青春版', 'Linux', 'iPhone', 'Google爬虫','Baidu爬虫']
	index = -1
	for d in konwns_rel_devices:
		index+=1
		if d in device:
			device = konwns_devices[index]
			break
	return device

def support_at(content):
	users = re.findall('@[^ @\r\n\t,]+ ', content)
	users = list(set(users))
	for user in users:
		content = content.replace(user, '<a href="/profile/%s">%s</a>' % (user[1:][:-1], user))
	return content

def from_topic_notify_user(content, title, id, conn):
	users = re.findall('@[^ @\r\n\t,]+ ', content)
	users = list(set(users))
	for user_raw in users:
		user = user_raw[1:-1]
		if user == session['ol_user']['name']:
			continue
		uid = conn.execute("select id from user where name='%s'" % user).first()[0]
		conn.execute("insert into message(content, from_id, to_id) values('[%(user)s](/profile/%(user)s)在发布主题[%(title)s](/t/%(id)d)时提到了你.', 1, %(uid)d)" % {'user':session['ol_user']['name'], 'title':title, 'id':id, 'uid':uid})

def from_answer_notify_user(content, title, id, conn):
	users = re.findall('@[^ @\r\n\t,]+ ', content)
	users = list(set(users))
	for user_raw in users:
		user = user_raw[1:-1]
		if user == session['ol_user']['name']:
			continue
		uid = conn.execute("select id from user where name='%s'" % user).first()[0]
		conn.execute("insert into message(content, from_id, to_id) values('[%(user)s](/profile/%(user)s)在主题[%(title)s](/t/%(id)d)的答案中提到了你.', 1, %(uid)d)" % {'user':session['ol_user']['name'], 'title':title, 'id':id, 'uid':uid})

def update_online_users(session, app, request, username = None):
	online_usernames = app.online_usernames
	online_users = app.online_users
	online_user_updates_queue = app.online_user_updates_queue
	def create_user(name, last_time):
		return {
			'name':name,
			'last_time':last_time
		}
	if 'ol_user' in session:
		username = session['ol_user']['name']
	else:
		if not username:
			username = request.cookies.get(app.session_cookie_name)
		if username:
			username = hashlib.md5(username.encode('utf-8')).hexdigest()
			username = username + ' • ' + get_post_device(request.headers.get('User_Agent')) + '用户'
	if username not in online_usernames:
		online_usernames.append(username)
		online_users.append(create_user(username, datetime.datetime.now()))
	else:
		online_user_updates_queue.put(username)

def create_recent_topic_item(row, conn):
	user = conn.execute('select id,`name`, avatar from user where id=%d' % row.author_id).first()
	forum = conn.execute('select id, `name` from forum where id=%d' % row.forum_id).first()
	answer_count = conn.execute('select count(id) from answer where topic_id=%d' % row.id).first()[0]
	answer_info = conn.execute('select post_date, author_id from answer where topic_id=%d order by post_date desc limit 1' % row.id).first()
	if answer_info:
		 answer_author = conn.execute('select id, `name`, avatar from user where id=%d' % answer_info.author_id).first()
	return {
		'title':row.title,
		'id':row.id,
		'post_date':get_date_fashion(row.post_date),
		'author':{
			'id':user.id,
			'name':user.name,
			'avatar':user.avatar
		},
		'forum':{
			'id':forum.id,
			'name':forum.name
		},
		'view_count':row.view_count,
		'answer_count':answer_count,
		'last_reply_date': get_date_fashion(answer_info.post_date) if answer_info else 'None',
		'last_reply_author': {
			'id':answer_author.id,
			'name':answer_author.name,
			'avatar':answer_author.avatar
		} if answer_info else 'None'
	}