#!/usr/bin/env python
import os
import tornado.ioloop
import tornado.web
from tornado.options import parse_command_line,define,options

define("host",default='localhost',help='主机地址',type=str)
define("port",default='8000',help='端口号',type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        abc = self.get_argument('arg','哈楼')
        sex = self.get_argument('sex','保密')
        name = self.get_argument('name','Admin')
        menu = ['红烧肉','水果莎拉','糖醋排骨','牛排','波士顿龙虾','三文鱼刺身']
        self.render("index.html",xyz=abc,name=name,sex=sex,menu=menu)

class BlockHandler(tornado.web.RequestHandler):
    def get(self):
        title = '草'
        content ='''
            离离原上草，
            一岁一枯荣，
            野火烧不尽，
            春风吹又生。
        '''
        self.render("article.html",title=title,content=content)


def make_app():
    routes=[
        (r"/", MainHandler),
        (r"/block", BlockHandler),
        (r"/test",StaticTestHandler),
    ]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir,'templates')
    static_dir = os.path.join(base_dir,'statics')
    return tornado.web.Application(routes,
                                   template_path = template_dir,
                                   static_path = static_dir)

class StaticTestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('static_test.html')

if __name__ == "__main__":
    parse_command_line()

    app = make_app()
    print('server running on %s:%s' % (options.host, options.port))
    app.listen(options.port, options.host)

    tornado.ioloop.IOLoop.current().start()


