import os, time
from threading import Thread
def init(app):
    plugin_data = os.getcwd() + '/data/good.tdb'
    if not os.path.exists(plugin_data):
        with open(plugin_data, 'w+') as f:
            f.write('[]')
        app.good_topic_ids = []
    else:
        def glist(f):
            item = f.readline().strip()[1:-1].split(", ")
            if item[0] != '':
                return list(map(int, item))
            return []
        with open(plugin_data) as f:
            app.good_topic_ids = glist(f)
    def run():
        Thread(target=save_good_topics).start()
    def save_good_topics():
        while True:
            time.sleep(600)
            with open(plugin_data, 'w+') as f:
                f.write(str(app.good_topic_ids))
    return run