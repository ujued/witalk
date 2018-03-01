import json
from flask import Blueprint, current_app, request, render_template, session, redirect
from tools import filter_sql, page_turning_info, get_date_fashion, get_post_device, support_at
from tools import update_online_users, create_recent_topic_item, from_answer_notify_user, from_topic_notify_user

bp = Blueprint('wit', __name__)

@bp.route('/')
def index():
	update_online_users(session, current_app, request)
	return render_template('index.html', all_focus="class='nd-focus'",lang_focus='',archer_focus='',qa_focus='',trade_focus='', quickindex = 'all')

@bp.route('/<node_name>')
def index__(node_name):
	update_online_users(session, current_app, request)
	all_focus = None
	programming_focus = None
	art_focus = None
	hot_focus = None
	trade_focus = None
	if node_name == 'all':
		all_focus = "class='nd-focus'"
	elif node_name == 'art':
		art_focus = "class='nd-focus'"
	elif node_name == 'programming':
		programming_focus = "class='nd-focus'"
	elif node_name == 'hot':
		hot_focus = "class='nd-focus'"
	elif node_name == 'trade':
		trade_focus = "class='nd-focus'"
	else:
		return render_template('404.html')
	return render_template('index.html', all_focus=all_focus,programming_focus=programming_focus,art_focus=art_focus,hot_focus=hot_focus,trade_focus=trade_focus, quickindex = node_name)

@bp.route('/forums')
def forums():
	update_online_users(session, current_app, request)
	return render_template('forums.html')

@bp.route('/new/<int:id>', methods = ['GET', 'POST'])
def post(id):
	conn = current_app.mysql_engine.connect()
	count = conn.execute('select count(id) from forum where id=%d' % id).first()[0]
	if count == 0:
		return render_template('404.html')
	forum = conn.execute('select id, name from forum where id=%d ' % id).first()
	if 'ol_user' not in session :
		return redirect('/passport/login')
	if request.method == 'GET':
		return render_template('new.html', param = None, forum = forum)
	user = session['ol_user']
	title = request.form['title']
	content = request.form['content']
	param = {
		'title':title,
		'content':content
	}
	if title is None or len(title) < 4 :
		message = '标题不能少与4字!'
	elif len(title) < 8 and (content is None or len(content) < 12):
		message = '标题少与8字时, 内容不能少于12字!'
	else:
		title, content, user_agent = filter_sql([title, content.replace('<', '&lt;').replace('>', '&gt;'), request.headers.get('User-Agent')])
		count = conn.execute("select count(id) from topic where title='%s'" % title).first()[0]
		if count != 0:
			message = '这篇主题发表过了!'
		else:
			rowcount = conn.execute("insert into topic(title, content, author_id, forum_id, user_agent) values('%s', '%s', %d, %d, '%s')" % (title, content, user['id'], id, user_agent)).rowcount
			if rowcount == 1:
				conn.execute('update user set points=points+2 where id=%d' % user['id'])
				
				# recent topics
				topic_id = conn.execute("select id from topic where title='%s'" % title).first()[0]
				if len(current_app.all_recent_topic_ids) == 24:
					current_app.all_recent_topic_ids.pop()
				current_app.all_recent_topic_ids.insert(0, topic_id)
				forumid = str(id)
				if forumid in current_app.programming_forum_ids.split(','):
					if len(current_app.programming_recent_topic_ids) == 24:
						current_app.programming_recent_topic_ids.pop()
					current_app.programming_recent_topic_ids.insert(0, topic_id)
				if forumid in current_app.art_forum_ids.split(','):
					if len(current_app.art_recent_topic_ids) == 24:
						current_app.art_recent_topic_ids.pop()
					current_app.art_recent_topic_ids.insert(0, topic_id)
				if forumid in current_app.trade_forum_ids.split(','):
					if len(current_app.trade_recent_topic_ids) == 24:
						current_app.trade_recent_topic_ids.pop()
					current_app.trade_recent_topic_ids.insert(0, topic_id)
				from_topic_notify_user(content, title, topic_id, conn)
				message = '创建成功!'
			else:
				message = '失败!'
		conn.close()
	return render_template('new.html', message = message, param = param, forum = forum)

@bp.route('/reply/<int:id>', methods = ['POST'])
def reply(id):
	conn = current_app.mysql_engine.connect()
	topic = conn.execute('select * from topic where id=%d' % id).first()
	if topic is None:
			return render_template('404.html')
	if 'ol_user' not in session:
		return redirect('/passport/login')
	content = request.form['content']
	param = {
		'content':content
	}
	user = session['ol_user']
	if content is None or len(content) < 1:
		message = '内容不能为空.'
	else:
		content, user_agent = filter_sql([content.replace('<', '&lt;').replace('>', '&gt;'), request.headers.get('User-Agent')])
		count = conn.execute("insert into answer(content, author_id, topic_id, user_agent) values('%s', %d, %d, '%s')" % (content, user['id'], id, user_agent)).rowcount
		if count == 1:
			# message = '回复成功.'
			conn.execute('update user set points=points+1 where id=%d' % user['id'])

			forumid = str(topic.forum_id)
			all_ids = current_app.all_recent_topic_ids
			programming_forumids = current_app.programming_forum_ids.split(',')
			programming_ids = current_app.programming_recent_topic_ids
			art_forumids = current_app.art_forum_ids.split(',')
			art_ids = current_app.art_recent_topic_ids
			trade_forumids = current_app.trade_forum_ids.split(',')
			trade_ids = current_app.trade_recent_topic_ids
			if topic.id in all_ids:
				all_ids.remove(topic.id)
			all_ids.insert(0, topic.id)
			if forumid in programming_forumids:
				if topic.id in programming_ids:
					programming_ids.remove(topic.id)
				programming_ids.insert(0, topic.id)
			if forumid in art_forumids:
				if topic.id in art_ids:
					art_ids.remove(topic.id)
				art_ids.insert(0, topic.id)
			if forumid in trade_forumids:
				if topic.id in trade_ids:
					trade_ids.remove(topic.id)
				trade_ids.insert(0, topic.id)
			from_answer_notify_user(content, topic.title, topic.id, conn)
			conn.close()
			return redirect('/t/%d' % id)
		else:
			message = '失败.'
	conn.close()
	return render_template('reply.html', message = message, topic = topic, param = param)

@bp.route('/f/<int:id>')
def list(id):
	update_online_users(session, current_app, request)
	conn = current_app.mysql_engine.connect()
	forum = conn.execute('select * from forum where id=%d' % id).first()
	topic_count = conn.execute('select count(id) from topic where forum_id=%d' % id).first()[0]
	if forum is None:
		return render_template('404.html')
	collected = False
	if 'ol_user' in session:
		if conn.execute("select count(id) from collection where collect_cate='f' and collect_id=%d and owner_id=%d" % (id, session['ol_user']['id'])).first()[0] != 0:
			collected = True
	conn.close()
	return render_template('forum.html', forum = forum, topic_count = topic_count, collected = collected)

def create_topic_item(row, conn):
	user = conn.execute('select id,`name`, avatar from user where id=%d' % row.author_id).first()
	user_dict = {
		'id':user.id,
		'name':user.name,
		'avatar':user.avatar
	}
	forum = conn.execute('select id, `name` from forum where id=%d' % row.forum_id).first()
	forum_dict = {
		'id':forum.id,
		'name':forum.name
	}
	answer_count = conn.execute('select count(id) from answer where topic_id=%d' % row.id).first()[0]
	return {
		'title':row.title,
		'id':row.id,
		'post_date':get_date_fashion(row.post_date),
		'author':user_dict,
		'forum':forum_dict,
		'view_count':row.view_count,
		'answer_count':answer_count
	}

@bp.route('/topics/<int:id>/<int:pid>')
def topics(id, pid):
	json_topics = []
	conn = current_app.mysql_engine.connect()
	if id == 0:
		count = conn.execute('select count(id) from topic').first()[0]
	else:
		count = conn.execute('select count(id) from topic where forum_id=%d' % id).first()[0]
	page_count = request.args.get('count')
	if page_count :
		page_info = page_turning_info(count, pid, int(page_count))
	else: 
		page_info = page_turning_info(count, pid)

	if not page_info['have']:
		return 'None'
	if id == 0:
		sql = 'select * from topic limit %s' % page_info['limit']
	else:
		sql = 'select * from topic where forum_id=%d limit %s' % (id, page_info['limit'])
	topics = conn.execute(sql).fetchall()
	topics.reverse()
	for topic in topics:
		json_topics.append(create_topic_item(topic, conn))
	conn.close()
	return json.dumps(json_topics, ensure_ascii = False)

@bp.route('/rtopics/<cate>')
def rtopics(cate):
	sql = 'select * from topic where id=null'
	if cate == 'all':
		for id in current_app.all_recent_topic_ids:
			sql += ' union select * from topic where id=%d' % id
	elif cate == 'programming':
		for id in current_app.programming_recent_topic_ids:
			sql += ' union select * from topic where id=%d' % id
	elif cate == 'art':
		for id in current_app.art_recent_topic_ids:
			sql += ' union select * from topic where id=%d' % id
	elif cate == 'trade':
		for id in current_app.trade_recent_topic_ids:
			sql += ' union select * from topic where id=%d' % id
	else:
		return 'None'
	conn = current_app.mysql_engine.connect()
	dumps_topics = []
	row = conn.execute(sql).fetchall()
	for t1 in row:
		dumps_topics.append(create_recent_topic_item(t1, conn))
	conn.close()
	return json.dumps(dumps_topics, ensure_ascii = False)

@bp.route('/mytopics/<int:uid>/<int:pid>')
def mytopics(uid, pid):
	json_topics = []
	conn = current_app.mysql_engine.connect()
	count = conn.execute('select count(id) from topic where author_id=%d' % uid).first()[0]
	if count == 0:
		return 'None'
	page_count = request.args.get('count')
	if page_count :
		page_info = page_turning_info(count, pid, int(page_count))
	else: 
		page_info = page_turning_info(count, pid)

	if not page_info['have']:
		return 'None'
	sql = 'select * from topic where author_id=%d limit %s' % (uid, page_info['limit'])
	topics = conn.execute(sql).fetchall()
	topics.reverse()
	for topic in topics:
		json_topics.append(create_topic_item(topic, conn))
	conn.close()
	return json.dumps(json_topics, ensure_ascii = False)

@bp.route('/t/<int:id>')
def view(id):
	update_online_users(session, current_app, request)
	conn = current_app.mysql_engine.connect()
	topic = conn.execute('select * from topic where id=%d' % id).first()
	if topic is None:
		return render_template('404.html')
	conn.execute('update topic set view_count=view_count+1 where id=%d' % id) # view_count
	forum = conn.execute('select id, name from forum where id=%d' % topic.forum_id).first()
	author = conn.execute('select id, name, avatar from user where id=%d' % topic.author_id).first()
	answer_count = conn.execute('select count(id) from answer where topic_id=%d' % topic.id).first()[0]
	last_answer_info_row = conn.execute('select author_id, post_date from answer where topic_id=%d order by post_date desc limit 1' % topic.id).first()
	if not last_answer_info_row:
		last_answer_info = None
	else:
		last_answer_author = conn.execute('select id, name from user where id=%d' % last_answer_info_row.author_id).first()
		last_answer_info = {
			'author_name':last_answer_author.name,
			'author_id':last_answer_author.id,
			'post_date':last_answer_info_row.post_date
		}
	collect_count = conn.execute("select count(id) from collection where collect_id=%d and collect_cate='t'" % id).first()[0]
	conn.close()
	return render_template('topic.html', topic = topic, forum = forum, author = author, answer_count = answer_count, collect_count = collect_count, last_answer_info = last_answer_info)

def create_answer_item(row, conn):
	user = conn.execute('select id,`name`, avatar from user where id=%d' % row.author_id).first()
	user_dict = {
		'id':user.id,
		'name':user.name,
		'avatar':user.avatar
	}
	return {
		'content':support_at(row.content),
		'post_date':get_date_fashion(row.post_date),
		'via': get_post_device(row.user_agent) if row.user_agent else 'unkonwn',
		'author':user_dict
	}

@bp.route('/answers/<int:id>/<int:pid>')
def answers(id, pid):
	json_answers = []
	conn = current_app.mysql_engine.connect()
	count = conn.execute('select count(id) from answer where topic_id=%d' % id).first()[0]
	page_info = page_turning_info(count, pid)
	if not page_info['have']:
		return 'None'
	answers = conn.execute('select * from answer where topic_id=%d limit %s' % (id, page_info['limit'])).fetchall()
	for answer in answers:
		json_answers.append(create_answer_item(answer, conn))
	conn.close()
	return json.dumps(json_answers, ensure_ascii = False)