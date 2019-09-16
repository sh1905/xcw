#!/usr/bin/env python

import tornado.ioloop
import tornado.websocket
from tornado.options import parse_command_line,define,options


define("host",default='localhost',help='主机地址',type=str)
define("port",default='8000',help='端口号',type=int)

class MsgHandler(tornado.websocket.WebSocketHandler):
    conn_pool = set()

    def open(self):
        print('客户端跟我建立连接')
        self.conn_pool.add(self)

    def on_message(self,message):
        print('收到了来自客户端的消息:%s' % message)
        #self.write_message('我收到了你的消息：%s' % message)
        self.broadcast(message)

    def on_close(self):
        print('客户端跟我断开连接')
        self.conn_pool.remove(self)
    def broadcast(self,message):
        '''广播消息'''
        for conn in self.conn_pool:
            if conn is not self:
                conn.write_message(message)

def make_app():
    return tornado.web.Application([
        (r"/msg",MsgHandler)
    ])

if __name__ == '__main__':
    parse_command_line()
    app = make_app()

    print('server running on %s:%s'% (options.host,options.port))
    app.listen(options.port,options.host)
    tornado.ioloop.IOLoop.current().start()


