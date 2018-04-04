from flask import Blueprint, current_app, request, render_template, redirect, session, flash, g
from tools import get_date_fashion, filter_sql
from witalk import create_topic_item
from services import svc_collection

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
	conn = current_app.connect()
	f_collections_row = conn.execute("select * from collection where collect_cate='f' and owner_id=%d" % user['id']).fetchall()
	t_collections_row = conn.execute("select * from collection where collect_cate='t' and owner_id=%d" % user['id']).fetchall()
	f_collections = []
	t_collections = []
	for collection in f_collections_row:
		f_collections.append(create_f_collection_item(collection, conn))
	for collection in t_collections_row:
		t_collections.append(create_t_collection_item(collection, conn))
	f_collections.reverse()
	t_collections.reverse()
	return render_template(g.tperfix + 'collections.html', f_collections = f_collections, t_collections = t_collections)

@bp.route('/collect/<cate>/<int:id>')
def collect(cate, id):
	if 'ol_user' not in session:
		return redirect('/login?back=/collections')
	cate, = filter_sql([cate,])
	
	if cate == 'nont' : svc_collection.noncollect('t', id)
	elif cate == 'nonf' : svc_collection.noncollect('f', id)
	else : svc_collection.collect(cate, id)

	backurl = request.args.get('back')
	if backurl:
		return redirect(backurl)
	else:
		return redirect('/collections')
