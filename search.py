from flask import Blueprint, current_app, request, render_template, session, redirect, g, flash, jsonify
bp = Blueprint('search', __name__)

@bp.route("/search")
def search():
	return render_template(g.tperfix + 'search.html')

@bp.route("/s", methods=['GET'])
def search_exe():
	word = request.args.get('wd')
	if not word:
		word = request.args.get('word')
	if not word:
		flash('请输入关键字进行筛选。多个关键字用空格隔开。')
		return redirect('/search')
	wds = word.split(' ')
	wt = weight()
	conn = current_app.mysql_engine.connect()
	for wd in wds:
		if wd == '':
			continue
		wdts = conn.execute("select id from topic where title like '%%%%%s%%%%' or content like '%%%%%s%%%%'" % (wd, wd)).fetchall()
		fid = conn.execute("select id from forum where name='%s'" % wd).first()
		if fid:
			ts = conn.execute("select id from topic where forum_id=%d" % fid[0]).fetchall()
			for t in ts:
				wt.add(t)		
		for wdt in wdts:
			wt.add(wdt)
	wt.calc_sort()
	sql = 'select id,title,author_id,forum_id,post_date,view_count from topic where id=null'
	for id in wt.value:
		sql += ' union select id,title,author_id,forum_id,post_date,view_count from topic where id=%d' % id
	topic_rows = conn.execute(sql).fetchall()
	conn.close()
	#for row in topic_rows:
	return render_template(g.tperfix + 'search.list.html', topics = topic_rows, word = word)	
		
class weight:
	def __init__(self):
		self.clear()
	def add(self, list):
		self.list.extend(list)
	def calc(self):
		self.reset()
		for item in self.list:
			if item in self.value:
				v = self.degree[self.value.index(item)]
				self.degree[self.value.index(item)] = v + 1
			else:
				self.value.append(item)
				self.degree.append(1)
	def sort(self):
		
		for i in range(len(self.degree)-1):
			for j in range(len(self.degree)-i-1):
				if self.degree[j] > self.degree[j+1]:
					self.degree[j], self.degree[j+1] = self.degree[j+1], self.degree[j]
					self.value[j], self.value[j+1] = self.value[j+1], self.value[j]
		self.value.reverse()
		self.degree.reverse()
	def calc_sort(self):
		self.reset()
		self.calc()
		self.sort()

	def reset(self):
		self.value = []
		self.degree = []
	def clear(self):
		self.reset()
		self.list = []
