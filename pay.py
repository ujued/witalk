from flask import Blueprint, request, session, redirect, current_app, render_template, flash, g
from tools import filter_sql
from services import svc_user, svc_topic
bp = Blueprint('pay', __name__)

@bp.route('/pay/<int:id>', methods = ['GET', 'POST'])
def pay(id):
	if 'ol_user' not in session:
		return redirect('/login?back=/pay/%d' % id)
	price_author = svc_topic.column('author_id, price', id)
	if price_author:
		if svc_user.check_bag('topic', id) or price_author.price == 0 or price_author.author_id == session['ol_user']['id']:
			return redirect('/t/%d' % id)
		if request.method == 'POST':
			price = price_author.price
			password = request.form['password']
			password, = filter_sql([password,])
			if svc_user.check_password(password):
				if svc_user.points() >= price:
					svc_user.update_points(-price, trade_info='pay for topic')
					svc_user.pack_bag('topic', id)
					svc_user.update_points(int(price * 0.9), uid=price_author.author_id)
					return redirect('/t/%d' % id)
				else:
					flash('你的T币不够了！')
			else:
				flash('密码错误！')
		return render_template(g.tperfix + 'pay.html', topicid = id)
	else:
		return render_template(g.tperfix + '404.html')
