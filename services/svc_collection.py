from flask import current_app, session, flash

def collected(cate, id):
    """
    return boolean
    """
    if 'ol_user' not in session:
        return False
    uid = session['ol_user']['id']
    conn = current_app.connect()
    count = conn.execute("select count(id) from collection where owner_id=%d and collect_cate='%s' and collect_id=%d" % (uid, cate, id)).first()[0]
    if count == 1:
        return True
    return False
def collect(cate, id, uid=None):
    """
    return None
    """
    if not uid:
        if 'ol_user' in session:
            uid = session['ol_user']['id']
        else : return
    conn = current_app.connect()
    count = conn.execute("select count(id) from collection where collect_cate='%s' and owner_id=%d and collect_id=%d" % (cate, uid, id)).first()[0]
    if count == 0:
        count = conn.execute("insert into collection(collect_cate, collect_id, owner_id) values('%s', %d, %d)" % (cate, id, uid)).rowcount
        if count == 1 : flash('收藏成功！')
        else : flash('收藏失败！')
    else : flash('已收藏！')
def noncollect(cate, id, uid=None):
    """
    return boolean
    """
    if not uid:
        if 'ol_user' in session : uid = session['ol_user']['id']
        else : return False
    conn = current_app.connect()
    count = conn.execute("delete from collection where collect_cate='%s' and collect_id=%d and owner_id=%d" % (cate, id, uid)).rowcount
    if count >= 1 : flash('取消收藏！')
    else : return flash('失败！')