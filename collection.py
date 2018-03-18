from flask import Blueprint, current_app, request, render_template, redirect, session, flash, g
from tools import get_date_fashion, filter_sql
from witalk import create_topic_item

bp = Blueprint('collection', __name__)

def create_f_collection_item(row, conn):
	forum = conn.execute('select * from forum where id=%d' % row.collect_id).first()
	return {
		'forum':{
			'id': forum.id,
			'name': forum.name
		},
		'collect_date': get_date_fashion(row.collect_date)
	}

def create_t_collection_item(row, conn):
	topic = conn.execute('select * from topic where id=%d' % row.collect_id).first()
	return {
		'topic':create_topic_item(topic, conn),
		'collect_date': get_date_fashion(row.collect_date)
	}
@bp.route('/collections')
def collections():
	if 'ol_user' not in session:
		return redirect('/login?back=/collections')
	user = session['ol_user']
	conn = current_app.mysql_engine.connect()
	f_collections_row = conn.execute("select * from collection where collect_cate='f' and owner_id=%d" % user['id']).fetchall()
	t_collections_row = conn.execute("select * from collection where collect_cate='t' and owner_id=%d" % user['id']).fetchall()
	f_collections = []
	t_collections = []
	for collection in f_collections_row:
		f_collections.append(create_f_collection_item(collection, conn))
	for collection in t_collections_row:
		t_collections.append(create_t_collection_item(collection, conn))
	conn.close()
	f_collections.reverse()
	t_collections.reverse()
	return render_template(g.tperfix + 'collections.html', f_collections = f_collections, t_collections = t_collections)

@bp.route('/collect/<cate>/<int:id>')
def collect(cate, id):
	if 'ol_user' not in session:
		return redirect('/login?back=/collections')
	user = session['ol_user']
	cate, = filter_sql([cate,])
	conn = current_app.mysql_engine.connect()
	count = conn.execute("select count(id) from collection where collect_cate='%s' and owner_id=%d and collect_id=%d" % (cate, user['id'], id)).first()[0]
	if count == 0:
		count = conn.execute("insert into collection(collect_cate, collect_id, owner_id) values('%s', %d, %d)" % (cate, id, user['id'])).rowcount
		if count == 1:
			flash('收藏成功！')
		else:
			flash('收藏失败！')
	else:
		flash('已收藏！')
	conn.close()
	backurl = request.args.get('back')
	if backurl:
		return redirect(backurl)
	else:
		return redirect('/collections')
