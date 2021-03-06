import time
from flask import Blueprint, request, render_template, redirect, session, current_app, make_response, Response, g, jsonify
from urllib import request as url_request
from urllib import error

bp = Blueprint('nav', __name__)

@bp.route('/privacy')
def privacy():
	return render_template(g.tperfix + 'privacy.html')

@bp.route('/about')
def about():
	return render_template(g.tperfix + 'about.html')

@bp.route('/thanks')
def thanks():
	return render_template(g.tperfix + 'thanks.html')

@bp.route('/onlines')
def onlines():
	return render_template(g.tperfix + 'onlines.html')



@bp.route('/img/<path:imgname>')
def images(imgname):
	exname = imgname.split('.')[-1]
	if exname == 'jpg':
		mimetype = 'image/jpeg'
	else:
		mimetype = 'image/' + exname

	try:
		with current_app.open_resource('images/' + imgname) as f:
			image = f.read()
	except FileNotFoundError:
		try:
			with url_request.urlopen('https://witalk-1252785209.cos.ap-hongkong.myqcloud.com/%s' % imgname) as f:
				image = f.read()
		except error.HTTPError:
			return render_template('404.html')
	resp = Response(image, mimetype = mimetype)
	return resp

@bp.route('/upload', methods = ['POST', 'GET'])
def upload():
	if 'ol_user' not in session:
		return redirect('/login?back=/upload')
	if request.method == 'GET':
		return render_template(g.tperfix + 'upload.html')
	file = request.files['image'];
	filename = str(time.time())
	filename += ('.' + file.filename.split('.')[-1])
	file.save("/opt/witalk/images/" + filename)
	conn = current_app.connect()
	conn.execute("insert into picture (name, author_id, size) value('%s', %d)" % (filename, session['ol_user']['id']))
	conn.close()
	return render_template(g.tperfix + 'upload.html', filename = filename)

@bp.route('/pictures')
def pictures():
	if 'ol_user' not in session:
		return redirect('/login?back=/pictures')
	conn = current_app.connect()
	pictures = conn.execute("select * from picture where author_id = %d" % session['ol_user']['id']).fetchall()
	conn.close()
	pictures.reverse()
	return render_template(g.tperfix + 'pictures.html', pictures = pictures)

@bp.route('/signin')
def signin():
	from services import svc_user
	result = svc_user.signin()
	if result == -1:
		return jsonify({'status':'offline'})
	if result == 0:
		return jsonify({'status':'repeat sign'})
	return jsonify({'status':'success', 'points':result})