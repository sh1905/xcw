#!/usr/bin/env python
import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler,Application
import pymysql

db = pymysql.connect(host='localhost',
                    user='xcw',
                    password='182562',
                    db='weekday3',
                    charset='utf8')
cur = db.cursor()

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument('id')
        sql = "select * from student where `id`=%s;"
        cur.execute(sql,str(id))
        db.commit()
        print(id)
        result=cur.fetchall()
        self.write(str(result))

def make_app():
    return tornado.web.Application([
        (r"/",TestHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()

db.close()
