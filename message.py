from flask import Blueprint, current_app, request, render_template, redirect, session, flash
from tools import get_date_fashion, filter_sql

bp = Blueprint('message', __name__)
def create_message_item(row, conn):
	from_user = conn.execute('select id,`name`,avatar from user where id=%d' % row.from_id).first()
	to_user = conn.execute('select id,`name`,avatar from user where id=%d' % row.to_id).first()
	return {
		'id':row.id,
		'content':row.content,
		'from_user':{
			'id':from_user.id,
			'name':from_user.name,
			'avatar':from_user.avatar
		},
		'to_user':{
			'id':to_user.id,
			'name':to_user.name,
			'avatar':to_user.avatar
		},
		'send_date': get_date_fashion(row.send_date)
	}

@bp.route('/msgbox')
def read_messages():
	if 'ol_user' not in session:
		return redirect('/login?back=/msgbox')
	user = session['ol_user']
	conn = current_app.mysql_engine.connect()
	read_messages = conn.execute('select * from message where to_id=%d and readed=0 and (first_del_id is null or first_del_id<>%d)' % (user['id'], user['id'])).fetchall()
	conn.execute('update message set readed=1 where to_id=%d and readed=0' % user['id'])
	messages = []
	for message in read_messages:
		messages.append(create_message_item(message, conn))
	conn.close()
	messages.reverse()
	return render_template('msgbox.html', receive = True, messages = messages, title='未读信息 • <a href="/msgbox/all">收件箱</a>&nbsp;&nbsp;<a href="/msgbox/send">发件箱</a>')

@bp.route('/msgbox/all')
def all_messages():
	if 'ol_user' not in session:
		return redirect('/login?back=/msgbox/all')
	user = session['ol_user']
	conn = current_app.mysql_engine.connect()
	all_messages = conn.execute('select * from message where to_id=%d and (first_del_id is null or first_del_id<>%d)' % (user['id'], user['id'])).fetchall()
	messages = []
	for message in all_messages:
		messages.append(create_message_item(message, conn))
	conn.close()
	messages.reverse()
	return render_template('msgbox.html', receive = True, messages = messages, title='收件箱 • <a href="/msgbox">未读信息</a>&nbsp;&nbsp;<a href="/msgbox/send">发件箱</a>')

@bp.route('/msgbox/send')
def send_messages():
	if 'ol_user' not in session:
		return redirect('/login?back=/msgbox/all')
	user = session['ol_user']
	conn = current_app.mysql_engine.connect()
	send_messages = conn.execute('select * from message where from_id=%d and (first_del_id is null or first_del_id<>%d)' % (user['id'], user['id'])).fetchall()
	messages = []
	for message in send_messages:
		messages.append(create_message_item(message, conn))
	conn.close()
	messages.reverse()
	return render_template('msgbox.html', noreply = True, send = True, messages = messages, title = '发件箱 • <a href="/msgbox">未读信息</a>&nbsp;&nbsp;<a href="/msgbox/all">收件箱</a>')

@bp.route('/msgsend', methods = ['POST', 'GET'])
def send_message():
	if 'ol_user' not in session:
		return redirect('/login?back=/msgsend')
	if request.method == 'GET':
		to_user = None
		if request.args.get('to'):
			to_user = request.args.get('to')
		import urllib
		to_user = urllib.parse.unquote(to_user)
		if "'" in to_user:
			return render_template('404.html')
		return render_template('msgsend.html', to_user = to_user)
	user = session['ol_user']
	to_user = request.form['username']
	msg_content = request.form['content']
	if to_user is None or msg_content is None or len(msg_content) < 1:
		return render_template('msgsend.html', message = '接收者不能为空，信息内容不能为空！')
	if to_user == user['name']:
		return render_template('msgsend.html', message = '不能给自己发信息！')
	to_user, msg_content = filter_sql([to_user, msg_content])
	conn = current_app.mysql_engine.connect()
	to_id_row = conn.execute("select id from user where name='%s'" % to_user).first()
	if not to_id_row:
		message = '接收者不存在！'
	else:
		count = conn.execute("insert into message(content, from_id, to_id) values('%s', %d, %d)" % (msg_content, user['id'], to_id_row.id)).rowcount
		if count == 1:
			message = '已发送！'
		else:
			message = 'Error.'
	conn.close()
	return render_template('msgsend.html', message = message)

@bp.route('/msgdel/<int:id>')
def msgdel(id):
	if 'ol_user' not in session:
		return redirect('/login')
	user = session['ol_user']
	conn = current_app.mysql_engine.connect()
	first_del_id = conn.execute('select first_del_id from message where id=%d and (from_id=%d or to_id=%d)' % (id, user['id'], user['id'])).first()[0]
	if first_del_id and (first_del_id != user['id']):
		conn.execute('delete from message where id=%d' % id)
	else:
		conn.execute('update message set first_del_id=%d where id=%d and (from_id=%d or to_id=%d)' % (user['id'], id, user['id'], user['id']))
	flash('已删除！')
	backurl = request.args.get('back')
	if backurl:
		return redirect(backurl)
	return redirect('/msgbox/all')