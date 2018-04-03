import os, time
from configuration import *
from threading import Thread
plugin_data = os.getcwd() + '/data/recent.tdb'
def init(app):
	app.programming_forum_ids = programming_forum_ids
	app.art_forum_ids = art_forum_ids
	app.trade_forum_ids = trade_forum_ids
	if not os.path.exists(plugin_data):
		app.all_recent_topic_ids = []
		app.programming_recent_topic_ids = []
		app.art_recent_topic_ids= []
		app.trade_recent_topic_ids = []
		with app.mysql_engine.connect() as conn:
			all_row = conn.execute('select id from topic order by post_date desc limit 36').fetchall()
			programming_row = conn.execute('select id from topic where forum_id in (%s) order by post_date desc limit 36' % programming_forum_ids).fetchall()
			art_row = conn.execute('select id from topic where forum_id in (%s) order by post_date desc limit 36' % art_forum_ids).fetchall()
			trade_row = conn.execute('select id from topic where forum_id in(%s) order by post_date desc limit 36' % trade_forum_ids).fetchall()
			for t1 in all_row:
				app.all_recent_topic_ids.append(t1.id)
			for t2 in programming_row:
				app.programming_recent_topic_ids.append(t2.id)
			for t3 in art_row:
				app.art_recent_topic_ids.append(t3.id)
			for t4 in trade_row:
				app.trade_recent_topic_ids.append(t4.id)
	else:
		def glist(f):
			item = f.readline().strip()[1:-1].split(", ")
			if item[0] != '':
				return list(map(int, item))
			return []
		with open(plugin_data) as f:
			app.all_recent_topic_ids = glist(f)
			app.programming_recent_topic_ids = glist(f)
			app.art_recent_topic_ids = glist(f)
			app.trade_recent_topic_ids = glist(f)
	def run():
		Thread(target=save_recent_topics).start()		
	def save_recent_topics():
		while True:
			time.sleep(600)
			with open(plugin_data, 'w+') as f:
				f.write(str(app.all_recent_topic_ids))
				f.write('\n')
				f.write(str(app.programming_recent_topic_ids))
				f.write('\n')
				f.write(str(app.art_recent_topic_ids))
				f.write('\n')
				f.write(str(app.trade_recent_topic_ids))
	return run