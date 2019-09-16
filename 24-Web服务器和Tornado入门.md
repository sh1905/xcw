HTTP 协议

- 构建在长链接的的基础上的短连接协议

TCP 协议

* 建立连接：三次握手

* 断开连接：四次挥手

* 可靠

* 长连接

```tex
URL资源定位

https/ftp/sockets/redis/mysql :端口号/绝对路径
query string
? q=Tornado&oq=Tornado #锚点
http方法的定义有两点：safe and Idempotent，即安全性和幂等性POST/DELETE/PUT/GET/PATCH/OPTION/HEAD

常见的局域网地址

`10.x.x.x`

`172.16.x.x-172.17.x.x`

`192.168.x.x`
```



## 一、HTTP 服务器

HTTP 协议是建立在 TCP 协议之上的短连接协议。
它利用了 TCP 协议的可靠性,用来传输超文本 (HTML),通信一次连接一次,通信完成后 TCP 连接关
闭。
所以如果想创建一个 HTTP Server 需要通过 Socket 搭建一个服务端程序。

```tex
步骤：
1.导入socket模块
	import socket
2.创建socket对象
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
3.绑定服务器地址
	sock.bind('0.0.0.0',8000)
4.设置监听队列
	sock.listen(100)
5.定义'响应报文'
    html = b'''
    HTTP/1.1 200 OK

    <html>
        <head>
            <title>home</title>
        </head>
        <body>
            Hello world
        </body>
    </html>
    '''
6.等待接受客户端连接
	cli_sock, cli_addr = sock.accept()
    # 第一个返回值是客户端的 socket 对象
    # 第二个返回值是客户端的地址
7.接收客户端传来的数据
	cli_data = cli_sock.recv(1024)
8.向客户端发送请求
	cli_sock.sendall(html)
9.断开与客户端的连接
	cli_sock.close()
```



### simple-server.py

```python
#!/usr/bin/env python
import socket
import time

addr = ('127.0.0.1', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 为 sock 打开地址可重用选项
sock.bind(addr)   # 绑定服务器地址
sock.listen(100)  # 设置监听队列
# 定义 "响应报文"
html = b'''
HTTP/1.1 200 OK

<html>
    <head>
        <title>home</title>
    </head>
    <body>
        Hello world
    </body>
</html>
'''
while True:
    print('服务器已运行，正在等待客户端连接。。。')
    # 等待接受客户端连接
    # 第一个返回值是客户端的 socket 对象
    # 第二个返回值是客户端的地址
    cli_sock, cli_addr = sock.accept()
    print('接收到来自客户端 %s:%s 的连接' % cli_addr)
    # 接收客户端传来的数据，1024是接收缓冲区的大小
    cli_data = cli_sock.recv(1024)
    print('接收到客户端发来的 "请求报文": \n%s' % cli_data.decode('utf8'))
    cli_sock.sendall(html)  # 向客户端发送数据
    # 断开与客户端的连接
    cli_sock.close()
    print('连接断开, 退出！')
```

### simple-server-2.py

```shell
#!/usr/bin/env python

import socket
import time

addr = ('127.0.0.1', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 为 sock 打开地址可重用选项
sock.bind(addr)   # 绑定服务器地址
sock.listen(100)  # 设置监听队列

# 定义 "响应报文"
template = '''
HTTP/1.1 200 OK

<html>
    <head>
        <title>home</title>
    </head>
    <body>%s</body>
</html>
'''


def get_url(request_str):
    '''从 "请求报文" 中获取请求的 URL'''
    first_line = request_str.split('\n')[0]  # 取出第一行
    url = first_line.split(' ')[1]  # 按空格切分，取出中间的 URL
    return url


while True:
    print('服务器已运行，正在等待客户端连接。。。')

    # 等待接受客户端连接
    # 第一个返回值是客户端的 socket 对象
    # 第二个返回值是客户端的地址
    cli_sock, cli_addr = sock.accept()
    print('接收到来自客户端 %s:%s 的连接' % cli_addr)

    # 接收客户端传来的数据，1024是接收缓冲区的大小
    cli_request = cli_sock.recv(1024).decode('utf8')
    print('接收到客户端发来的 "请求报文": \n%s' % cli_request)

    # 获取用户的 URL
    url = get_url(cli_request)

    # 根据 URL 生成不同的返回值
    if url == '/foo':
        response = template % '爱妃退下，朕在调戏代码'
    elif url == '/bar':
        response = template % '姜伟老师没醉过，但求一醉'
    else:
        response = template % 'hello world'

    print(url, response)
    cli_sock.sendall(response.encode('utf8'))  # 向客户端发送数据

    # 断开与客户端的连接
    cli_sock.close()
    print('连接断开, 退出！')

```

```python
request_str='''
GET / HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
'''

def get_url(request_str):
    first_line=request_str.strip().split('\n')[0]
    url=first_line.split('')[1]
    return url
```



```html
'<form action="/test/post" method="post">'
    '姓名:<input type="text" name="name">'
    '<br/>'
    '城市:<input type="text" name="city">'
    '<input type='submit'>'
'</form>'
```

对 SimpleServer 进行扩展

根据不同 URL 显示不同页面

页面整体样式不变,根据不同参数,从数据库中取出不同学生信息,并填充到页面中







## 二、Web 框架概述

随着技术的发展,我们每天的要处理的信息量都在爆炸新的增加。传统的静态页面技术早已跟不上时代
需求,因而催生了动态页面技术。
所谓动态页面,即所有的页面用程序来生成,以细节实现上的不同,又可分为“前端动态页面”和“后端动态页面”。

 Web 前端阶段所学 Ajax、VUE 等技术,就是前端动态页面。而今后我们所学的主要是后端动态页面技术,甚至是两者结合使用。

### 1.Web服务器原理

![1568036900007](./images/1568036900007.png)

### 2.常见的 Web 框架

如果想完成更复杂的功能,还需要深入开发很多东西,比如模版系统、ORM系统、路由系统、会话机制。

| 框架        | **描述**                                                     |
| ----------- | ------------------------------------------------------------ |
| **Django**  | 全能型框架，大而全，插件丰富，文档丰富，社区活跃, 适合快速开发, 内部耦合比较紧 |
| **Flask**   | 微型框架, 适合新手学习, 极其灵活, 便于二次开发和扩展, 生态环境好, 插件丰富 |
| **Tornado** | 异步处理, 事件驱动 (epoll), 性能优异                         |
| Bottle      | 单文件框架, 结构紧凑,适合初学者阅读源码,了解 Web 原理        |
| web.py      | 代码优美, 且适合学习源码                                     |
| Falcon      | 性能优异适合写 API 接口                                      |
| Quixote     | 一个爷爷级别的框架,著名的豆瓣网用的便是这个                  |
| Sanic       | 后起之秀,性能秒杀以上所有前辈,但没有前辈们稳定。             |



## 三、Tornado入门

### 1.安装

```shell
pip install tornado
```

### 2.helloword实例

```python
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello,World')
def make_app():
    return tornado.web.Application([
        (r"/",MainHandler),
    ])

if __name == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```

### 3.启动参数

```python
from tornado.option import parse_command_line,define,options

define("host",default='0.0.0.0',help="主机地址",type=str)
define("port",default=8888,help="主机端口"，type=int)
parse_command_line()

print('传入的主机：%s' % options.host)
print('传入的端口：%s' % options.post)
```

### 4.路由处理

```python
import tornado.ioloop
from tornado.web import RequestHandler, Application

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("欢迎进入主页")

class BookHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("你想看的书应有尽有")
app = Application([
    (r'/',HomeHandler),
    (r'/book/',BookHandler)
])

app.listen(8000)
tornado.ioloop.IOLoop.curren().start()
```

### 5.处理GET和POST请求

```python
class TestPostHandler(tornado.web.RequestHandler):
    def get(self):
        html = '''
			<form action="/test/post" method="POST">
            姓名: <input type="text" name="name">
            <br />
            城市: <input type="text" name="city">
            <br />
            <input type="submit">
            </form>
        '''
        self.write(html)
    def post(self):
        name = self.get_argument('name')
        city = self.get_argument('city')
        self.write('%s 生活在 %s'%(name,city))
        
app = listen(8000)
tornado.ioloop.IOLoop.current().start()
```

### HTTP的请求方法：

| Method  | Description                                                  |
| ------- | ------------------------------------------------------------ |
| POST    | 向指定资源提交数据进行处理请求，数据被包含在请求体中         |
| GET     | 请求指定的页面信息，并返回实体主体                           |
| PUT     | 从客户端向服务器传送的数据取代指定的文档的内容               |
| DELETE  | 请求服务器删除指定的页面                                     |
| HEAD    | 类似于GET请求，只不过返回的响应中没有具体的内容，用于获取报头 |
| PATCH   | 是对PUT方法的补充，用来对资源进行局部更新。                  |
| OPTIONS | 允许客户端查看服务器的性能。                                 |



### demo.py

```python
#!/usr/bin/env python

import tornado.ioloop
import tornado.web
from tornado.options import parse_command_line, define, options

define("host", default='localhost', help="主机地址", type=str)
define("port", default=8000, help="主机端口", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class AifeiHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("爱妃退下，朕在调戏代码")


class JiangPangpangHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("姜伟老师没醉过，但求一醉")


class TestGetHandler(tornado.web.RequestHandler):
    def get(self):
        # 接收 URL 中的参数
        name = self.get_argument('name')
        self.write("%s但求一醉" % name)


class TestPostHandler(tornado.web.RequestHandler):
    def get(self):
        html = '''
            <form action="/test/post" method="POST"> 
            姓名: <input type="text" name="name">
            <br>
            城市: <input type="text" name="city">
            <input type="submit">
            </form>
        '''
        self.write(html)

    def post(self):
        name = self.get_argument('name')
        city = self.get_argument('city')

        self.write('%s 生活在 %s' % (name, city))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/foo", AifeiHandler),
        (r"/bar", JiangPangpangHandler),
        (r"/test/get", TestGetHandler),
        (r"/test/post", TestPostHandler),
    ])


if __name__ == "__main__":
    parse_command_line()

    app = make_app()
    print('server running on %s:%s' % (options.host, options.port))
    app.listen(options.port, options.host)

    loop = tornado.ioloop.IOLoop.current()
    loop.start()

```

```shell
python demo.py --host=127.0.0.1 --port=8000
```

















