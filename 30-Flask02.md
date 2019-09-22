```python
"existing endpoint function: %s" % endpoint
AssertionError: View function mapping is overwriting an existing endpoint function: blue.testResponse
视图函数重名
raise BuildError(endpoint, values, method, self)
werkzeug.routing.BuildError: Could not build url for endpoint 'blue.testReverse'. Did you mean 'first.testReverse' instead?
蓝图名错误
```



## 一、Request

### 1、request是一个内置对象

内置对象：不需要创建就可以直接使用的对象

### 2、内置属性

```python
1. method（请求方法）**
2. base_url（去掉get参数的URL）
3. host_url（只有主机和端口号的URL）
4. url（完整的请求地址）**
5. remote_addr（请求的客户端地址）**
6. request.args.get('name')（获取get请求的参数）
    - args
    - get请求参数的包装，args是一个ImmutableMultiDict对象，类字典结构对象
    - 数据存储也是key-value
    - 外层是大列表，列表中的元素是元组，元组中左边是key，右边是value
    - ImmutableMultiDict([('age', '18'), ('age', '19'), ('name', 'zs')])

    注意： 一般情况下,get请求方式都是在浏览器的地址栏上显示
    eg：http：//www.baiduc.com/s?name=zs&age=18
    获取get请求方式的参数的方式：request.args.get('name')
          
7. request.form.get('name')（获取post）
    - form
    - 存储结构和args一致
    - 默认是接收post参数
    - 还可以接收 PUT，PATCH参数
    注意：eg：
    <form action='xxx' method='post'>
    <input type='text' name='name'>
    获取post请求方式的参数的方式
8. files（文件上传）**
9. header（请求头）
10. path（路由中的路径）**
11. cookies（请求中的cookie）
12. sessions（与request类似，也是一个内置对象，可以直接打印 print(session)）
```

实例：

```python
# mysql 3306 mongodb 27017  oracle 1521 redis 6379
# http 80  https 443
# ftp 21 ssh 22 
```

```python

@blue.route('/testRequest/',methods=['post','get'])
def testRequest():
    
@blue.route('/testRequest/',methods=['post','get'])
def testRequest():
    # 获取的是请求方式/http方法
    print(request.method)

    # 去掉请求参数的路径
    # http://127.0.0.1:5000/testRequest/
    print(request.base_url)

    # http://127.0.0.1:5000/
    # 主机的路径不带请求资源路径
    print(request.host_url)

    # http://127.0.0.1:5000/testRequest/?name=zs
    # 完整的url路径（请求资源路径，请求参数）
    print(request.url)

    # 主机地址  应用场景  反爬虫
    print(request.remote_addr)

    # 应用场景 文件上传
    print(request.files)

    # 请求头
    print(request.headers)

    # 请求资源路径   应用场景：购物车
    print(request.path)

    # 获取请求的cookies
    print(request.cookies)


    # http://127.0.0.1:5000/testRequest/?name=zs
    # 怎么获取name的值
    print(request.args)
    name = request.args.get('name')
    print(name)
    age = request.args.get('age')
    print(age)
	# http://127.0.0.1:5000/testRequest/?name=zs
    age1 = request.args.getlist('age')
    print(age1)


    # 获取post请求的参数
    name2 = request.form.get('name')
    print(name2)

    age2 = request.form.get('age')
    print(age2)

    age3 = request.form.getlist('age')
    print(age3)

    return 'testRequest'

    # 获取的是请求方式/http方法
    print(request.method)

    # 去掉请求参数的路径
    # http://127.0.0.1:5000/testRequest/
    print(request.base_url)

    # http://127.0.0.1:5000/
    # 主机的路径不带请求资源路径
    print(request.host_url)

    # http://127.0.0.1:5000/testRequest/?name=zs
    # 完整的url路径（请求资源路径，请求参数）
    print(request.url)

    # 主机地址  应用场景  反爬虫
    print(request.remote_addr)

    # 应用场景 文件上传
    print(request.files)

    # 请求头
    print(request.headers)

    # 请求资源路径   应用场景：购物车
    print(request.path)

    # 获取请求的cookies
    print(request.cookies)


    # http://127.0.0.1:5000/testRequest/?name=zs
    # 怎么获取name的值
    print(request.args)
    name = request.args.get('name')
    print(name)
    age = request.args.get('age')
    print(age)

    age1 = request.args.getlist('age')
    print(age1)


    # 获取post请求的参数
    name2 = request.form.get('name')
    print(name2)

    age2 = request.form.get('age')
    print(age2)

    age3 = request.form.getlist('age')
    print(age3)

    return 'testRequest'
```

## 二、Response视图函数的返回值类型

### 1、返回字符串

### 2、render_template渲染模板

### 3、make_response 

### 4、redirect 重定向

### 5、Response

```python
# 视图函数返回字符串
@blue.route('/testResponse/')
def testResponse():
    return '窗前明月光'


# 视图函数返回一个模板
@blue.route('/testResponse2/')
def testResponse2():
    s = render_template('testResponse2.html')
    print(type(s))
    return s

# 视图函数返回一个make_response()
@blue.route('/testResponse3/')
def testResponse3():
    r = make_response('<h1>举头望明月</h1>')
    print(type(r))
    return r

# 视图函数返回redirect
@blue.route('/index/')
def index():
    return 'welcome to 东北'

@blue.route('/testResponse4/')
def testResponse4():
    # r = redirect('/index/')# 重定向 
    r = redirect(url_for('blue.index'))# 反向解析 
    print(type(r))
    return r

# 视图函数返回Response对象
@blue.route('/testResponse5/')
def testResponse5():
    r = Response('低头思故乡')
    print(type(r))
    return r
```

### 总结：视图函数的返回值有2大类

* 字符串
  * 普通字符串
  * **render_template**
* response对象
  * make_response
  * **redirect**
  * Response

## 三、异常

### 1、abort

* 直接抛出异常，显示错误状态码，终止程序运行，abort(404)

```python
@blue.route('/testAbort/')
def testAbort():
    abort(404)
    return 'testAbort'
```

### 2、异常捕获

* 可以根据状态码或**Exception**进行捕获

* 函数中要包含一个参数，参数用来接收异常信息

```python
@blue.errorhandler(404)
def testAbort1(Exception):
    return '系统升级,请稍候再试!'
```

## 四、会话技术

```python
1.请求过程从Request开始，到Response结束
2.连接都是短连接
3.延长交互的生命周期
4.将关键数据记录下来
5.Cookie是保存在浏览器端/客户端的状态管理技术
6.Session是服务器端的状态管理技术
```

### 1、Cookie

```tes
1.客户端会话技术
2.所有数据存储在客户端
3.以key-value进行数据存储层
4.服务器不做任何存储
5.特性
    (1)支持过期时间
        max_age  毫秒
        expries  具体日期
    (2)根据域名进行cookie存储
    (3)不能跨网站（域名）
    (4)不能跨浏览器
    (5)自动携带本网站的所有cookie
6.cookie是服务器操作客户端的数据
7.通过Response进行操作
```

```python
cookie  视图函数登陆使用
1.设置cookie     response.set_cookie('username',username)
2.获取cookie     username = request.cookies.get('username','游客')
3.删除cookie     response.delete_cookie('username')
```

```python
# cookie的使用
# 需求：执行一个视图函数tologincookie  跳转到一个页面logincookie.html
#      输入一个用户名字xxx  点击提交  跳转到welcomecookie.html
#      该页面的内容是 欢迎xxx光临red romance。。。。
#      如果没有经过登录  直接跳转到welcomecookie.html 会显示 欢迎游客光临
#      如果已经登录然后跳转到welcomecookie.html 那么在欢迎xxx的下面
#      还有一个退出  然后退出  跳转到welcomecookie.html页面
#      显示 欢迎游客。。。

@blue.route('/tologincookie/')
def tologincookie():
    return render_template('logincookie.html')

@blue.route('/logincookie/',methods=['post'])
def logincookie():
    # ‘name’ 是input标签的name的属性值
    name = request.form.get('name')

    response = redirect(url_for('blue.welcomecookie'))
    # response = redirect('/welcomecookie/')
    # 设置cookie必须要有response对象   那么response对象的获取有三种方式
    # 分别为make_response，redirect,Response()
    # 如果我们选择make_response方法  那么make_response('<>')  x
    # 如果我们选择Response方法      那么Reseponse('fdffdf')   x
    # ‘name’  key值,可以随便定义; name 在前端获取的name值
    response.set_cookie('name',name)

    return response

@blue.route('/welcomecookie/')
def welcomecookie():

    # 获取cookie中的name
    # ‘name’ cookie的key值
    name = request.cookies.get('name','游客')

    return render_template('welcomecookie.html',name=name)


@blue.route('/logoutcookie/')
def logoutcookie():

    response = redirect(url_for('blue.welcomecookie'))

    response.delete_cookie('name')
    return response
```

### 2、Session

```python
1.服务端会话技术
2.所有数据存储在服务器中
3.默认存在服务器的内存中
- django默认做了数据持久化（存在了数据库中）
4.存储结构也是key-value形势，键值对
【注】单纯的使用session是会报错的，需要使用在__init__方法中配置app.config['SECRET_KEY']='110'
```

```python
session  视图函数登陆使用
1.设置    session['name'] = name
2.获取    session.get('name')
3.删除    session.pop('name') 
		或者
	   response.delete_cookie('session')
```

```python
@blue.route('/tologinsession/')
def tologinsession():
    return render_template('loginsession.html')

@blue.route('/loginsession/',methods=['post'])
def loginsession():
    name = request.form.get('name')
    session['name'] = name
    return redirect(url_for('blue.welcomesession'))

@blue.route('/welcomesession/')
def welcomesession():
    name = session.get('name','游客')
    return render_template('welcomesession.html',name=name)

@blue.route('/logoutsession/')
def logoutsession():
    response = redirect(url_for('blue.welcomesession'))
    response.delete_cookie('session')
    # session.pop('name')
    return response
```



### 3、cookie和session总结

```tex
1. cookie：客户端浏览器的缓存；session：服务端服务器的缓存
2. cookie：不是很安全，别人可以解析存放在本地的cookie并进行cookie欺骗，考虑到安全应当使用session
3. session会在一定时间内保存在服务器上。当访问增多，会比较占用你服务器的性能，考虑到减轻服务器性能方面，应当使用cookie
   可以考虑将登陆信息等重要信息存放为session，其他信息如果需要保留，可以放在cookie中
```



### 4、session持久化问题

* 持久化简介

  ```tex
  1.django中对session做了持久化处理，存储在数据库中
  2.flask中没有对默认session进行任何处理
  	- flask-session 可以实现session的数据持久化
  	- 可以持久化到任何位置，推荐使用Redis数据库
  	- 缓存到磁盘上的时候，管理磁盘文件使用lru,最少使用原则
  ```

* 持久化实现方案

  ```tex
  1.使用pip install flask-session
  	或者使用国内源 pip install flasksessin -i https://pipy.douban.com/simple
  	
  2.初始化Session对象
  (1)持久化的位置
  在 __init__.py中配置 
  	app.config['SESSION_TYPE']='redis'
  	
  (2)初始化
  创建session对象有两种方式：
  	1 Session(app=app)常用
  	2 session=Session() -> session.init_app(app=app)
  	
  (3)安装Redis
  pip install redis -> apt install redis
  
  (4)需要在__init__.py中配置 
  app.config['SECRET_KEY']='110'
  
  注意：flask把session的key存储在客户端的cookie中，通过这个key可以从flask的内存中获取用户的session信息，出于安全性考虑，使用secret_key进行加密处理。所以需要先设置secret_key的值。
  
  (5)其他配置->视情况而定				app.config['SESSION_KEY_PREFIX']='flask'		
  特殊说明：
  redis-cli    登录
  keys *       查看所有的键
  get key      获取键对应的value
  ttl session  查看存活时间
  (flask的session的生存时间是31天，django的session生存时间是14天)
  ```

```python
# __init__.py
from flask import Flask
from flask_session import Session

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='110'
    # 如果报错 No module named 'redis'那么证明虚拟环境中没有redis模块
    # 需要我们手动安装pip install redis
    # session的生命周期是31天
    app.config['SESSION_TYPE']='redis'
    # 在redis中keys * 显示前缀 'flask'
    app.config['SESSION_KEY_PREFIX']='flask1905/'
    # Session(app=app)
    session = Session()
    session.init_app(app=app)
    return app
```



## 五、Template

### 1、简介

* MVC中的View，MTV中的Template
* 主要用来做数据展示
* 模板处理的过程分为2个阶段
  * 1	加载
  * 2    渲染
* jinjia2模板引擎
  * 本质上是HTML
  * 支持特定的模板语法
  * Flask作者开发的一个现代化和友好的python模板语言，模仿Django的模板引擎
* 优点
  * 速度快，被广泛使用
  * HTML设计和后端python分离
  * 减少Python的复杂度
  * 非常灵活，快速和安全
  * 提供了控制，继承等高级功能

**定界符：**

（1）语句
比如if判断、for循环等：

        {% ... %}
（2）表达式
比如字符串、变量、函数调用等：

        {{ ... }}
（3）注释

        {# ... #}

### 2、模板语法

#### 1.基本语法

```python
模板语言动态生成的html
{{ var }} => 变量的接收
从views传递过来的数据
前面定义出来的数据

# 模板的基本使用
@blue.route('/index/')
def index():
    # 优化  (1)页面接收,视图函数没有传递
    #      (2)视图函数传递, 页面没有接收
    return render_template('index.html',age=18,sex='male')
```

#### 2.结构标签

```tex
（1）block
    继承父模板时，和子模块的block重名，加{{ super() }}是追加，不加是覆盖。
    {% block header  %}
        绵绵的青山脚下花正开
    {% endblock %}
（2）extends 继承父模板
	{% extends 'base.html' %}
（3）include 包含，将一个指定的模板包含进来
    {% block footer  %}
        {{ super() }}
        {% include 'base_x.html' %}
    {% endblock%}
    {# 注释 #}
```

#### 3.宏定义（macro）

```tex
(1)无参数
	{% macro say() %}
    	一经发现,严惩不贷!
    {% endmacro  %}
	{{ say() }}
	
(2)有参数
	{% macro getUser(name,age)%}
    	{{ name }}的年龄是{{ age }}
    {% endmacro %}

    {{ getUser('zhangsan',18) }}
    
(3外文件中的宏定义调用需要导入也可以include
testMacro1.html
{% macro getName() %}
    违法记录
{% endmacro %}

testMacro.html
{% from 'testMacro1.html' import getName %}
-----------------------------------------
{% macro getUser(name)%}
	欢迎光临红浪漫{{ name }},拖鞋手牌拿好,楼上2楼左转,男宾一位。
{% endmacro %}

{% from ‘html文件’ import getUser %}
{{ getUser('张三') }}
需要传入函数对象本身，而不是函数调用（函数的返回值），所以仅写出函数名称即可。当把函数传入模板后，我们可以像在Python脚本中一样通过添加括号的方式调用，而且你也可以在括号中传入参数。
```

#### 4.循环控制

```tex
for
    for .. in 
        loop  循环信息
            index索引     
            first第一个    
            last最后一个 
    endfor
if
    if
    elif
    else  
    endif
```

![](./imgs/1568911293.jpeg)

```python
# 循环控制
@blue.route('/testFor/')
def testFor():
    score_list = [59,67,85,40,100]
    return render_template('testFor.html',score_list=score_list)
```

```html
<ul>
    {% for score in score_list %}
    	<li>{{ score }}</li>
    {% endfor %}
</ul>
<hr>
<ul>
    {% for score in score_list %}
    	{% if loop.first %}
    		<li style="color:green">{{ score }}</li>
    	{% elif loop.last %}
    		<li style="color:red">{{ score }}</li>
    	{% else %}
    		<li style="color:pink">{{ score }}</li>
    	{% endif %}
    {% endfor %}
</ul>
	{% for score in score_list %}
		{{ loop.index }}
	{% endfor %}
<hr />
	{% for score in score_list %}
		{{ loop.index0 }}
	{% endfor %}
<hr >
{% for score in score_list %}
	{{ loop.revindex }}
{% endfor %}
<hr>
{% for score in score_list %}
	{{ loop.revindex0 }}
{% endfor %}
```

#### 5.过滤器

   ```tex
   语法格式：{{ var|xxx|yyy|zzz }}
   没有数量限制
   		lower		小写
   		upper		大写
   		trim		去除两端空格
   		reverse		倒置
   		striptags   渲染之前将值中的标签去掉
   		safe        标签生效
   {% for c in config %}
       <li>{{ loop.index0 }}:{{ loop.index}}:{{ c|lower|reverse }}</li>
   {% endfor %}
   ```

  ![](./imgs/1568913458.jpeg)



 实例：

   ```python
   # 过滤器
   @blue.route('/testFilter/')
   def testFilter():
       code ='abcdefghijklmn'
       code1 = 'abcd    '
       code2 = '<h1>cdef</h1>'
       return render_template('testFilter.html',code=code,code1=code1,code2=code2)
   ```

   ```html
   现在天气适合出去旅游,不适合上课!
   <hr>
   {{ code|upper }}
   <hr>
   {{ code|lower }}
   <hr>
   {{ code1|trim|reverse }}
   <hr>
   {{ code2 }}
   {{ code2|striptags }}
   <hr>
   {{ code2|safe }}
   ```

## 六、models

### 1、简介

```tex
1.数据交互的封装
2.Flask默认并没有提供任何数据库操作的API
	- Flask中可以自己的选择数据，用原生语句实现功能
		原生SQL缺点:
              (1)代码利用率低，条件复杂代码语句越过长，有很多相似语句
              (2)一些SQL是在业务逻辑中拼出来的，修改需要了解业务逻辑
              (3)直接写SQL容易忽视SQL问题
	- 也可以选择ORM
		1 SQLAlchemy
		2 MongoEngine
		将对象的操作转换为原生SQL
		优点:
			 (1)易用性，可以有效减少重复SQL
             (2)性能损耗少
             (3)设计灵活，可以轻松实现复杂查询
             (4)移植性好
3.Flask中并没有提供默认ORM
	- ORM 对象关系映射
	- 通过操作对象，实现对数据的操作
```

### 2、sqlalchemy

```python
1.pip install flask-sqlalchemy
2.创建SQLALCHEMY对象
      db=SQLAlchemy(app=app)
      -----------------------
      在models中书写 db=SQLAlchemy() -
      在init文件中db.init_app(app=app)，因为需要db来调 
3.config中配置  SQLALCHEMY_DATABASE_URI
数据库 + 驱动 :// 用户:密码@ 主机:端口/数据库
     dialect+driver://username:password@host:port/database
mysql+pymysql://xcw:182562@localhost:3306/day031905
4.执行
    views 中 db.create_all()
注意：
（1）primary-key 添加主键
（2）字符串要指定长度
（3）如果报错：'SQLALCHEMY_TRACK_MODIFICATIONS'
在__init__.py中书写
app.config[‘SQLALCHEMY_TRACK_MODIFICATIONS’]=False  
```



#### 使用步骤：


```tex
(1)定义模型
继承Sqlalchemy对象中的model
    eg:
    class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)l
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
(2)创建
	db.create_all()
(3)删除
	db.drop_all()
(4)修改表名
	__tablename__ = "animal1"
(5)数据操作
添加
    db.session.add(对象)
    db.session.commit()
查询
	表类.query.all()
```

```python
from flask import Blueprint, render_template, request, url_for, session
from App import db
from App.models import Animal
blue = Blueprint('blue',__name__)

# 通过模型创建表
@blue.route('/createTable/')
def createTable():
    db.create_all()
    return '创建成功'
# 通过模型删除表
@blue.route('/dropTable/')
def dropTable():
    db.drop_all()
    return '删除成功'
# 通过模型添加数据
@blue.route('/addanimal/')
def addanimal():
    a = Animal()
    a.name = 'hen'
    a.color = 'yellow'
    db.session.add(a)

    db.session.commit()
    return '添加成功'
# 通过模型查询所有的数据
@blue.route('/findall/')

def findall():
    animal_list = Animal.query.all()
    for animal in animal_list:
        print(animal.name)
    return '查询成功'

```

```python
# __init__.py
from flask import Flask
from App.models import db

def create_app():
    app = Flask(__name__)
      app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://xcw:182562@localhost:3306/students'   app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.init_app(app)
    return app
```

