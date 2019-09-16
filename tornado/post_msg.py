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
        html = '''
            <form action="/test/post" method="POST">
            要修改的姓名: <input type="text" name="name">
            <br/>
            性别:	<input type="text" name="sex">
            <br/>
            城市: <input type="text" name="city">
            <br/>
            描述:	<input type="text" name="description">
            <br/>
            <input type="submit">
            </form>
        '''
        self.write(html)

    def post(self):
        name = self.get_argument('name')
        sex = self.get_argument('sex')
        city = self.get_argument('city')
        description = self.get_argument('description')
        print(name,sex,city,description)
        sql = "update student set sex=%s,city=%s,description=%s where name=%s"
        cur.execute(sql,(str(sex),str(city),str(description),str(name)))
        db.commit()
        print('修改成功')



def make_app():
    return tornado.web.Application([
        (r"/test/post",TestHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()

db.close()
