import json, markdown2
from flask import Blueprint, current_app, request, render_template, session, redirect, g, flash, jsonify
from tools import *
from services import svc_user, svc_topic

bp = Blueprint('wit', __name__)

@bp.route('/')
def index():
	return render_template(g.tperfix + 'index.html', quickindex = 'all')

@bp.route('/<node_name>')
def index__(node_name):
	if node_name not in {'all', 'programming', 'art', 'trade', 'hot', 'good', 'paid'}:
		return render_template(g.tperfix + '404.html')
	return render_template(g.tperfix + 'index.html', quickindex = node_name)

@bp.route('/new/<int:id>', methods = ['GET', 'POST'])
def post(id):
	conn = current_app.connect()
	count = conn.execute('select count(id) from forum where id=%d' % id).first()[0]
	if count == 0:
		return render_template('404.html')
	forum = conn.execute('select id, name from forum where id=%d ' % id).first()
	if 'ol_user' not in session :
		return redirect('/login?back=/new/%d' % id)
	if request.method == 'GET':
		return render_template(g.tperfix + 'new.html', param = None, forum = forum)
	user = session['ol_user']
	title = request.form['title']
	content = request.form['content']
	price = request.form.get('price', '0')
	if not price.isdigit():
		price = 0
	else:
		price = int(price)
	param = {
		'title':title,
		'content':content,
		'price':price
	}
	if title is None or len(title) < 4 :
		message = '标题不能少与4字!'
	elif len(title) < 8 and (content is None or len(content) < 12):
		message = '标题少与8字时, 内容不能少于12字!'
	else:
		title, content, user_agent = filter_sql([title, content, request.headers.get('User-Agent')])
		count = conn.execute("select count(id) from topic where title='%s'" % title).first()[0]
		if count != 0:
			message = '这篇主题发表过了!'
		else:
			rowcount = conn.execute("insert into topic(title, content, author_id, forum_id, user_agent, price) values('%s', '%s', %d, %d, '%s', %d)" % (title, content, user['id'], id, user_agent, price)).rowcount
			if rowcount == 1:
				svc_user.update_points(+2, trade_info = 'post a topic')				
				# recent topics
				topic_id = conn.execute("select id from topic where title='%s'" % title).first()[0]
				ensure_recent_queue_when_post(topic_id, str(id))
				new_topic_notify(content, title, topic_id, conn)
				message = '创建成功!'
			else:
				message = '失败!'
	return render_template(g.tperfix + 'new.html', message = message, param = param, forum = forum)

@bp.route('/reply/<int:id>', methods = ['POST'])
def reply(id):
	conn = current_app.connect()
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
			svc_user.update_points(+1, trade_info = 'post a answer')
			forumid = str(topic.forum_id)
			ensure_recent_queue_when_reply(topic.id, forumid)
			new_answer_notify(content, topic.title, topic.id, conn)
			conn.close()
			return redirect('/t/%d' % id)
		else:
			message = '失败.'
	return render_template('reply.html', message = message, topic = topic, param = param)

@bp.route('/f/<int:id>')
def _list(id):
	conn = current_app.connect()
	forum = conn.execute('select * from forum where id=%d' % id).first()
	topic_count = conn.execute('select count(id) from topic where forum_id=%d' % id).first()[0]
	if forum is None:
		return render_template('404.html')
	collected = False
	if 'ol_user' in session:
		if conn.execute("select count(id) from collection where collect_cate='f' and collect_id=%d and owner_id=%d" % (id, session['ol_user']['id'])).first()[0] != 0:
			collected = True
	return render_template(g.tperfix + 'forum.html', forum = forum, topic_count = topic_count)

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
	conn = current_app.connect()
	if id == 0 : count = conn.execute('select count(id) from topic').first()[0]
	elif id == 1000 : count = len(current_app.good_topic_ids) # good
	elif id == 1001 : count = conn.execute('select count(id) from topic where view_count > 200').first()[0] # hot
	else : count = conn.execute('select count(id) from topic where forum_id=%d' % id).first()[0]
	page_count = request.args.get('count')
	if page_count :
		page_info = page_turning_info(count, pid, int(page_count))
	else: 
		page_info = page_turning_info(count, pid)

	if not page_info['have'] : return jsonify([])
	if id == 0 : sql = 'select * from topic limit %s' % page_info['limit']
	elif id == 1000:
		sql = 'select * from topic where id=null'
		l = list(map(int, page_info['limit'].split(', ')))
		limit_list = current_app.good_topic_ids[l[0]:l[1]]
		for id in limit_list:
			sql += ' union select * from topic where id=%d' % id
	elif id == 1001 : sql = 'select * from topic where view_count > 200 order by view_count desc'
	else : sql = 'select * from topic where forum_id=%d limit %s' % (id, page_info['limit'])
	topics = conn.execute(sql).fetchall()
	topics.reverse()
	json_topics = []
	for topic in topics:
		json_topics.append(create_topic_item(topic, conn))
	return jsonify(json_topics)

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
	elif cate == 'paid':
		for id in current_app.paid_recent_topic_ids:
			sql += ' union select * from topic where id=%d' % id
	else:
		return jsonify([])
	conn = current_app.connect()
	dumps_topics = []
	row = conn.execute(sql).fetchall()
	for t1 in row:
		dumps_topics.append(create_recent_topic_item(t1, conn))
	return jsonify(dumps_topics)

@bp.route('/mytopics/<int:uid>/<int:pid>')
def mytopics(uid, pid):
	json_topics = []
	conn = current_app.connect()
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
	return jsonify(json_topics)

def create_append_item(row, conn):
	user = conn.execute('select id, name, avatar from user where id=%d' % row.author_id).first()
	return{
		'author':{
			'id': user.id,
			'name':user.name,
			'avatar':user.avatar
		},
		'date':get_date_fashion(row.append_date),
		'content':row.append_content
	}

@bp.route('/t/<int:id>')
def view(id):
	conn = current_app.connect()
	topic = conn.execute('select topic.id,view_count,topic.user_agent,topic.post_date,title,price,content,user.name author_name,user.avatar author_avatar, user.id author_id, forum.name forum_name, forum.id forum_id from topic left join user on topic.author_id = user.id left join forum  on topic.forum_id = forum.id where topic.id=%d' % id).first()
	if topic is None:
		flash('主题不存在，可能因违法被回收！')
		return render_template(g.tperfix + '404.html')
	conn.execute('update topic set view_count=view_count+1 where id=%d' % id) # view_count
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
	auth_operate = check_topic_append(id, conn)
	auth_operate += check_auth_topic(id, topic.forum_id, conn)
	appends_row = conn.execute('select * from append_topic where topic_id=%d' % id)
	appends = []
	for append_row in appends_row:
		appends.append(create_append_item(append_row, conn))
	
	paymentIsOK = False
	if 'ol_user' in session and topic.price > 0:
		count = conn.execute("select count(id) from bag where user_id=%d and goods_name='topic' and goods_id=%d" % (session['ol_user']['id'], id)).first()[0]
		if count == 1:
			paymentIsOK = True
	return render_template(g.tperfix + 'topic.html', topic = topic, answer_count = answer_count, collect_count = collect_count,
		last_answer_info = last_answer_info, auth_operate = auth_operate, appends = appends, paymentIsOK = paymentIsOK)

def create_answer_item(row, conn):
	user = conn.execute('select id,`name`, avatar from user where id=%d' % row.author_id).first()
	user_dict = {
		'id':user.id,
		'name':user.name,
		'avatar':user.avatar
	}
	return {
		'content':support_at(markdown2.markdown(row.content)),
		'post_date':get_date_fashion(row.post_date),
		'via': get_post_device(row.user_agent) if row.user_agent else 'unkonwn',
		'author':user_dict
	}

@bp.route('/answers/<int:id>/<int:pid>')
def answers(id, pid):
	conn = current_app.connect()
	count = conn.execute('select count(id) from answer where topic_id=%d' % id).first()[0]
	page_info = page_turning_info(count, pid)
	if not page_info['have']:
		conn.close()
		return 'None'
	answers = conn.execute('select * from answer where topic_id=%d limit %s' % (id, page_info['limit'])).fetchall()
	json_answers = []
	for answer in answers:
		json_answers.append(create_answer_item(answer, conn))
	conn.close()
	return json.dumps(json_answers, ensure_ascii = False)

def create_own_answer_item(row, conn):
	topic = conn.execute("select id, title, author_id from topic where id=%d" % row.topic_id).first()
	if not topic:
		topic = conn.execute("select id, title, author_id from topic_trash where id=%d" % row.topic_id).first()
	author = conn.execute("select id, name, avatar from user where id=%d" % topic.author_id).first()
	return {
		'content':support_at(markdown2.markdown(row.content)),
		'post_date':get_date_fashion(row.post_date),
		'via': get_post_device(row.user_agent) if row.user_agent else 'unkonwn',
		'topic':{
			'title':topic.title,
			'id':topic.id,
			'author':{
				'name':author.name,
				'id':author.id,
				'avatar':author.avatar
			}
		}
	}
@bp.route("/own_answers/<int:uid>/<int:pid>")
def own_answers(uid, pid):
	conn = current_app.connect()
	count = conn.execute("select count(id) from answer where author_id=%d" % uid).first()[0]
	page_info = page_turning_info(count, pid)
	if not page_info['have']:
		conn.close()
		return 'None'
	answers = conn.execute('select * from answer where author_id=%d limit %s' % (uid, page_info['limit'])).fetchall()
	json_answers = []
	for answer in answers:
		json_answers.append(create_own_answer_item(answer, conn))
	conn.close()
	json_answers.reverse()
	return jsonify(json_answers)

@bp.route('/topicdel/<int:id>')
def topicdel(id):
	conn = current_app.connect()
	forum_id = conn.execute('select forum_id from topic where id=%d' % id).first()
	if forum_id == None:
		flash('主题已移入回收站，或没有发布！')
		return redirect('/t/%d' % id)
	else:
		forum_id = forum_id[0]
	auth = check_auth_topic(id, forum_id, conn)
	if auth != '':
		if conn.execute('insert into topic_trash select * from topic where id=%d' % id).rowcount == 1:
			conn.execute('delete from topic where id=%d' % id)
			ensure_recent_queue_when_remove(id)
			flash('主题已移入回收站！')
		else:
			flash('错误！')
	else:
		flash('不允许的操作！你没有权限！')
	conn.close()
	return redirect('/t/%d' % id)

@bp.route('/append/<int:id>', methods = ['POST', 'GET'])
def append(id):
	if 'ol_user' not in session:
		return redirect('/login?back=/append/%d' % id)
	conn = current_app.connect()
	auth_html = check_topic_append(id, conn)
	if auth_html == '':
		flash('无权操作！')
		conn.close()
		return render_template(g.tperfix + '404.html')
	topic = conn.execute('select id, title from topic where id=%d' % id).first()
	append_content = ''
	if request.method == 'POST':
		append_content = request.form['content']
		if append_content:
			append_content, = filter_sql([append_content,])
		else:
			flash('无效请求！')
			conn.close()
			return render_template(g.tperfix + '404.html')
		if len(append_content) < 6:
			flash('追加内容不得少于6字！')
		else:
			count = conn.execute("insert into append_topic(append_content, author_id, topic_id) values('%s', %d, %d)" % (append_content, session['ol_user']['id'], id)).rowcount
			if count == 1:
				flash('续贴成功！')
				conn.close()
				return redirect('/t/%d' % id)
			else:
				flash('error.')
	conn.close()
	return render_template(g.tperfix + 'append.html', topic = topic, content = append_content)
@bp.route('/forums')
def forums():
	conn = current_app.connect()
	forum_count = conn.execute('select count(id) from forum').first()[0]
	topic_count = conn.execute('select count(id) from topic').first()[0]
	trash_topic_count = conn.execute('select count(id) from topic_trash').first()[0]
	conn.close()
	return render_template(g.tperfix + 'forums.html', forum_count = forum_count, topic_count = topic_count, trash_topic_count = trash_topic_count)
@bp.route('/good/<op>/<int:id>')
def good_operate(op, id):
	if 'ol_user' in session and svc_user.administrator(): 
		svc_topic.good_operate(op, id)
	return redirect('/t/%d' % id)