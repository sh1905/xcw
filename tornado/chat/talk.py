#!/usr/bin/env python
import os
import logging

import tornado.ioloop
import tornado.websocket
from tornado.options import parse_command_line,define,options

from views import MainHandler,ChatSocketHandler

define("host",default='localhost',help='主机地址',type=str)
define("port",default='8000',help='端口号',type=int)



def main():
    parse_command_line()

    web_app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "statics"),
    )
    web_app.listen(options.port, options.host)

    logging.info('Server running on %s:%s' % (options.host, options.port))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()


