import hashlib
from flask import Blueprint, current_app, request, render_template, session, redirect, flash
from tools import filter_sql, update_online_users

bp = Blueprint('passport', __name__)

def create_user_dict(row):
	return {
		'id': row.id,
		'name': row.name,
		'email': row.email,
		'gender': row.gender,
		'age': row.age,
		'points': row.points,
		'signature': row.signature,
		'avatar': row.avatar,
		'my_page': row.my_page,
		'location':row.location,
		'github_name':row.github_name
	}

@bp.route('/login', methods = ['GET', 'POST'])
def  login():
	if request.method == 'GET':
		update_online_users(session, current_app, request)
		return render_template('login.html')
	id = request.form['id']
	password = request.form['password']
	if id == None or len(id) < 1 :
		message = '帐号不能为空！'
	elif password == None or len(password) < 6:
		message = "密码不少与6位！"
	else:
		id, password = filter_sql([id, password])
		password = hashlib.md5(password.encode('utf-8')).hexdigest()
		conn = current_app.mysql_engine.connect()
		if id.isdigit() :
			user_from_db = conn.execute("select * from user where id=%d  and password='%s'" % (id, password)).first()
		else:
			user_from_db = conn.execute("select * from user where (name='%s' or email='%s') and password='%s'" % (id, id, password)).first()
		conn.close()
		if user_from_db == None:
			message = '帐号或密码错误！'
		else:
			session['ol_user'] = create_user_dict(user_from_db)
			backurl= request.args.get('back')
			if backurl:
				return redirect(backurl)
			return redirect('/home')
	return render_template('login.html', message = message)

@bp.route('/register', methods = ['POST', 'GET'])
def register():
	if request.method == 'GET':
		update_online_users(session, current_app, request)
		return render_template('register.html')
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	if username == None or len(username) < 1 or username.isdigit() :
		message = '用户名不能为空或者数字.'
	elif password == None or len(password) < 6:
		message = "密码不能少于6位."
	elif email == None or len(email) < 8 or '@' not in email:
		message = 'Email是否正确？'
	else:
		conn = current_app.mysql_engine.connect()
		username, email, password  = filter_sql([username, email, password])
		password = hashlib.md5(password.encode('utf-8')).hexdigest()
		user_from_db = conn.execute("select id from user where name='%s' or email='%s'" % (username, email)).first()
		if user_from_db == None :
			count = conn.execute("insert into user(name, password, email) values('%s', '%s', '%s')" % (username, password, email)).rowcount
			referee = request.args.get('r')
			if referee and conn.execute("select count(id) from user where `name`='%s'" % referee).first()[0] == 1:
				referee, = filter_sql([referee,])
				conn.execute("update user set referee= '%s', points=points+5 where `name`='%s'" % (referee, username))
				conn.execute("update user set points=points+5 where `name`='%s'" % referee)
			if count == 1:
				message = '注册成功 ^_^'
			else:
				message = '注册失败！'
		else:
			message = '你注册过啦！可以用邮箱找回凭证。'
		conn.close()
	return render_template('register.html', message = message)

@bp.route('/profile/<int:id>')
def profile(id):
	update_online_users(session, current_app, request)
	conn = current_app.mysql_engine.connect()
	user_row = conn.execute('select id, name, gender, age, email, register_date, avatar, points,signature, my_page, github_name, location from user where id=%d' % id).first()
	if user_row == None:
		conn.close()
		return render_template('404.html')
	conn.close()
	online_usernames = current_app.online_usernames
	if user_row.name in online_usernames:
		user_online = True
	else:
		user_online = False
	return render_template('profile.html', user = user_row, user_online = user_online)

@bp.route('/profile/<username>')
def profile_name(username):
	update_online_users(session, current_app, request)
	import urllib
	username = urllib.parse.unquote(username)
	if "'" in username:
		return render_template('404.html')
	conn = current_app.mysql_engine.connect()
	user_row = conn.execute("select id, name, gender, age, email, register_date, avatar, points,signature, my_page, github_name, location from user where `name`='%s'" % username).first()
	if user_row == None:
		conn.close()
		return render_template('404.html')
	conn.close()
	online_usernames = current_app.online_usernames
	if user_row.name in online_usernames:
		user_online = True
	else:
		user_online = False
	return render_template('profile.html', user = user_row, user_online = user_online)

@bp.route('/home')
def home():
	update_online_users(session, current_app, request)
	if 'ol_user' not in session :
		return redirect('/login')
	conn = current_app.mysql_engine.connect()
	user = conn.execute('select id,avatar,points,name,age,gender,signature,my_page,email, location, github_name from user where id=%d' % session['ol_user']['id']).first()
	conn.close()
	return render_template('home.html', user = user)

@bp.route('/chinfo', methods = ['POST'])
def chinfo():
	if 'ol_user' not in session:
		return redirect('/login')
	avatar = request.form['avatar']
	if avatar[0:5] != 'https':
		flash('头像必须用https开头的ssl链接.')
		return redirect('/home')
	my_page = request.form['my_page']
	signature = request.form['signature']
	age = request.form['age']
	gender = request.form['gender']
	github_name = request.form['github']
	location = request.form['location']
	avatar, my_page, signature, age, gender, github_name, location= filter_sql([avatar, my_page, signature, age, gender, github_name, location])
	sets = 'id=%d' % session['ol_user']['id']
	if avatar != None and len(avatar)>0:
		sets += ", avatar='%s'" % avatar
	if my_page != None and len(my_page)>0:
		sets+= ", my_page='%s'" % my_page
	if signature != None and len(signature)>0:
		sets += ", signature='%s'" % signature
	if age != None and len(age)>0:
		sets += ", age=%d" % int(age)
	if gender != None and len(gender)>0:
		sets += ", gender='%s'" % gender
	if github_name != None and len(github_name)>0:
		sets += ", github_name='%s'" % github_name
	if location != None and len(location)>0:
		sets += ", location='%s'" % location
	conn = current_app.mysql_engine.connect()
	count = conn.execute('update user set %s where id=%d' % (sets, session['ol_user']['id'])).rowcount
	conn.close()
	if count == 1:
		session.pop('ol_user', None)
		flash('修改成功！请重新登录.')
		return redirect('/login')
	else:
		return 'error.'

@bp.route('/chpasswd', methods = ['POST'])
def chpasswd():
	if 'ol_user' not in session:
		return redirect('/login')
	oldpasswd = request.form['oldpasswd']
	newpasswd = request.form['newpasswd']
	renewpasswd = request.form['renewpasswd']
	oldpasswd, newpasswd, renewpasswd = filter_sql([oldpasswd, newpasswd, renewpasswd])
	if oldpasswd != None and len(oldpasswd) >= 6 and newpasswd != None and renewpasswd != None and len(newpasswd) >= 6 and len(renewpasswd) >= 6:
		if newpasswd == renewpasswd:
			conn = current_app.mysql_engine.connect()
			uid = session['ol_user']['id']
			if hashlib.md5(oldpasswd.encode('utf-8')).hexdigest() != conn.execute('select password from user where id=%d' % uid).first()[0]:
				flash('修改失败，密码错误！')
				conn.close()
				return redirect('/home')
			newpasswd = hashlib.md5(newpasswd.encode('utf-8')).hexdigest()
			count = conn.execute("update user set `password`='%s' where id=%d" % (newpasswd, uid)).rowcount
			conn.close()
			if count == 1:
				session.pop('ol_user', None)
				flash('修改成功！请重新登录.')
				return redirect('/login')
			else:
				return 'error.'
		else:
			flash('两次新密码不一致!')
			return redirect('/home')
	else:
		flash('安全起见，密码不得少于6位！')
		return redirect('/home')

@bp.route('/logout')
def logout():
	session.pop('ol_user', None)
	if request.args.get('back'):
		return redirect(request.args.get('back'))
	return redirect('/login')

@bp.route('/backpasswd')
def backpasswd():
	return render_template('backpasswd.html', message = '系统异常！密码找回系统暂无法使用！')