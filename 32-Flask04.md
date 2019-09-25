```tex
内聚：度量一个模块内部各个元素彼此结合的紧密程度。
耦合：度量模块之间互相连接的紧密程度。
目的：增强程序模块的可重用性、移植性。
```



## 一、分页器的相关方法

```tex
BaseQuery.paginate()
	page		  (页数)
	per-page	  (每一页的数量)
	False
Pagination
	items		  （遍历数据）
    pages         （获取总页数）
    prev_num      （上一页的页码）
    has_prev      （是否有上一页）
    next_num      （下一个页码）
    has_next	  （是否有下一页）
    iter_pages	  （上一页和下一页之间的页码）
```

```python
# views.py
@blue.route('/bootstrapDemo/')
def bootstrapDemo():
    page = int(request.args.get('page',1))
    per_page = request.args.get('per_page',5)

    pagination = Movie1.query.paginate(page=page,per_page=per_page)

    return render_template('bootstrapDemo.html',pagination=pagination,page=page)
```

```html
<!--bootstrapDemo.html-->

{% if pagination.has_prev %}
    <a href="{{ url_for('blue.bootstrapDemo') }}?page={{ pagination.prev_num }}" style="margin-left: 600px">上一页</a>
{% else %}
	<a href="#" style="margin-left: 600px">上一页</a>
{% endif %}

{% for p in pagination.iter_pages() %}
    {% if p == page %}
    	<a href="{{ url_for('blue.bootstrapDemo') }}?page={{ p }}" class="btn-success">{{ p }}</a>
    {% else %}
    	<a href="{{ url_for('blue.bootstrapDemo') }}?page={{ p }}" class="bg-danger">{{ p }}</a>
    {% endif %}

{% endfor %}


{% if pagination.has_next %}
	<a href="{{ url_for('blue.bootstrapDemo') }}?page={{ pagination.next_num }}">下一页</a>
{% else %}
	<a href="#">下一页</a>
{% endif %}
```



## 二、flask-bootstrap

```tex
1.插件安装
	pip install flask-bootstrap
2.ext 中初始化
	Bootstrap(app=app)
3.bootstrap案例-->bootstrap模板
	{% extends 'bootstrap/base.html' %}
```



## 三、flask-debugtoolbar =>辅助调试插件

```tex
1.安装
	pip install flask-debugtoolbar
2.初始化 ext
	app.debug = True   最新版本
	debugtoolbar = DebugToolBarExtension()
	debugtoolbar.init_app(app=app)
```

## 四、缓存flask-cache

```tex
1 缓存目的：
	缓存优化加载，减少数据库的IO操作
2 实现方案
    （1）数据库
    （2）文件
    （3）内存
    （4）内存中的数据库 Redis
3 实现流程
    （1）从路由函数进入程序
    （2）路由函数到视图函数
    （3）视图函数去缓存中查找
    （4）缓存中找到，直接进行数据返回
    （5）如果没找到，去数据库中查找
    （6）查找到之后，添加到缓存中
    （7）返回到页面上
4 使用
	（1）安装 flask-cache
		pip  install flask-cache
	（2）初始化 在第三方扩展库ext.py文件里
		目的：指定使用的缓存方案(数据库)
        cache = Cache(config={'CACHE_TYPE':'redis'[,默认是simple]})放在def方法外当做全局变量
        ---------------------------
        cache.init_app(app=app)在def方法内
    （3）使用
        1 装饰器@cache.cached(timeout=xxx)
        注意：装饰器必须放在视图函数路由的下面
        实例：
            @blue.route('/helloCache/')
            @cache.cached(timeout=30)
            def helloCache():
                print('这么多年总算看到了秋天')
            	return 'helloCache'
        2 原生代码
            cache.get()
            cache.set()
```



```python
# 1.缓存装饰器
# 放在视图函数路由上面或者下面,对视图函数没有影响;但是只有放在下面才能让timeout起作用。
# 30s后再次刷新浏览器，不会再打印  “秋天来了”，放在缓存中，有就不再读取。
from App.ext import cache

@blue.route('/helloCache/')
@cache.cached(timeout=30)
def helloCache():
    print('秋天来了!')
    return 'helloCache'

# 2.缓存原生
@blue.route('/testCache/')
def testCache():
    # 需求:第一次访问 显示  欢迎光临
    #      第二次访问 显示 小爬虫快走开
    value = cache.get('ip')
    if value:
        return '小爬虫快走开'
    else:
        # 根据IP判断是第几次访问
        ip = request.remote_addr
        cache.set('ip',ip)
    return '欢迎光临'
```

```python
# =======flask和flask_cache版本不兼容============
# ext.py
如果cache在方法内 那么导包是不可以的  
需要将 cache = Cache(config={'CACHE_TYPE':'redis'})遍历放到def方法外
如果报错 ImportError: No module named 'flask.ext'
解决方法：  (1)打开site-packages
          (2) flask-cache下的jinja2ext.py
          (3) 修改
# from flask.ext.cache import make_template_fragment_key
为from flask_cache import make_template_fragment_key
```



## 五、钩子

```python
# ============================
# 钩子 代码执行过程中添加了另一个方法的执行
# AOP 面向切面编程
# 如果在每个方法中添加了# print('链接数据库')  那么代码过于冗余
# 如果在每个方法中调用了# getConn()   那么代码依赖性过强
# 使用钩子的好处：解耦合，在请求之前去执行

def getConn():
    print('连接数据库')
# 一定不要加括号  before_request()
@blue.before_request
def beforeRequest():
    print('连接数据库!!!!')

@blue.route('/add/')
def add():
    # print('连接数据库')
    # getConn()
    return 'add'

@blue.route('/delete/')
def delete():
    # print('连接数据库')
    # getConn()
    return 'delete'

@blue.route('/update/')
def update():
    # print('连接数据库')
    return 'update'

@blue.route('/find/')
def find():
    # print('连接数据库')
    # getConn()
    return 'find'
```



## 六、四大内置对象

```tex
1.request
	请求的所有信息
2.session
	服务端会话技术的接口
3.config
	概念：当前项目的配置信息
    (1)模板中可以直接使用 config
    实例:
    {% for c in config %}
    <li>{{ c|lower }}</li>
    {% endfor %}

    (2)在python代码中  current_app.config
    实例:
    for c in current_app.config:
    	print(c)
4.g
    global  全局,可以帮助开发者实现跨函数传递数据
    实例:
    @blue.route('/g/')
    def g():
    g.ip = request.remote_addr
    return 'ok'

    @blue.route('/testg1/')
    def testg1():
    print(g.ip)
    return 'ok1'
```



```python
# ===================================
# 四大内置对象 request session config g
# 模板中config
@blue.route('/testTemConfig/')
def testTemConfig():
    return render_template('testTemConfig.html')

# python代码中的config
@blue.route('/testPythonConfig/')
def testPythonConfig():
    for c in current_app.config:
        print(c)
    return 'config:当前项目的配置信息'
# g
@blue.route('/g/')
def g():
    g.ip = request.remote_addr
    return 'g'
@blue.route('/testG/')
def testG():
    print(g.ip)
    return 'testG'
```



## 七、路径

* views.py

  ```python
  # template 和static 的路径问题
  @blue.route('/index/')
  def index():
      return render_template('index.html')
  ```

* __init__.py

  ```python
  import os
  
  from flask import Flask
  
  # flask-script flask-blueprint flask-session flask-sqlalchemy
  from App import settings
  from App.ext import init_ext
  template_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'templates')
  static_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'static')
  
  def create_app(env_name):
      app = Flask(__name__,template_folder=template_folder,static_folder=static_folder)
      
      app.config.from_object(settings.ENV_NAME.get(env_name))
      # db.init_app(app=app)
  
      # 获取当前文件的路径
      # a = os.path.abspath(__file__)
      # print(a)
      # 获取当前文件的路径的上一级路径
      # b = os.path.dirname(os.path.abspath(__file__))
      # print(b)
  
      # 先配置session和sqlalchemy,后初始化app
      init_ext(app)
      return app
  ```

* index.html

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>Title</title>
  </head>
  <body>
      诛仙1
  </body>
  </html>
  ```

## 八、前后端分离

```tex
整合网络和软件的一种架构模式
理解
	Representtational
		表现层
	State Transfer
		状态转换
	表现层状态转换
		资源（Resource）
	每一个URI代表一类资源
		对整个数据的操作
		增删改查
RESTful中更推荐使用HTTP的请求谓词（动词）来作为动作标识:
	GET   请求：查
	POST  发送：增
	PUT   修改全部
	DELETE   删除
	PATCH 修改部分
推荐使用json数据传输
```

```tex
=============为什么会出现Restful==============

1.在Restful之前的操作：
saveUser  表征性状态转移
http://127.0.0.1/user/query/1  GET  根据用户id查询用户数据
http://127.0.0.1/user/save     POST  新增用户
http://127.0.0.1/user/update   POST 修改用户信息
http://127.0.0.1/user/delete   GET/POST 删除用户信息

2.在Restful之后的操作：
http://127.0.0.1/user/ 根据请求方式的不同 那么执行不同的函数
    如果是get请求    那么执行的就是查询
    如果是post请求   那么执行的就是添加
    如果是put请求    那么执行的就是修改
    如果是delete请求 那么执行的就是删除
```



## 九、前后端分离--->原生代码

### 概念：

```
概念：就是判断不同的请求方式，实现请求方法
高内聚，低耦合
	高内聚
	相同的数据操作封装在一起
	低耦合
MVC 没有模板--前后端分离
弊端：1 判断请求方式
     2 使用jsonify序列化
```

get：

```
# 注意：判断请求方式的时候，请求方式必须大写
@blue.route("/users/<int:id>/", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def users(id):
    if request.method == "GET":
        page = int(request.args.get("page", default=1))
        per_page = int(request.args.get("per_page", default=3))

    users = User.query.paginate(page=page, per_page=per_page, error_out=False).items
    users_dict = []
    for user in users:
        users_dict.append(user.to_dict())

    data = {
    "message": "ok",
    "status": "200",
    "data": users_dict
    }

    return jsonify(data)
```

post：

```
elif request.method == "POST":
	# 更新或创建
    username = request.form.get("username")
    password = request.form.get("password")

    data = {
    "message": "ok",
    "status": "422"
    }

if not username or not password:
    data["message"] = "参数不正确"
    return jsonify(data), 422

user = User()
user.u_name = username
user.u_password = generate_password(password=password)

try:
    db.session.add(user)
    db.session.commit()
    data["status"] = "201"
except Exception as e:
    data["status"] = "901"
    data["message"] = str(e)
    return jsonify(data), 422

return jsonify(data), 201
```

put:

```
elif request.method == "PUT":
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.get(id)

    user.u_name = username
    user.u_password = generate_password(password)

    db.session.add(user)
    db.session.commit()

    data = {
    "message": "update success",
    }

    return jsonify(data), 201
```

delete:

```
elif request.method == "DELETE":
    user = User.query.get(id)

    data = {
    "message": "delete success"
    }

if user:
    db.session.delete(user)
    db.session.commit()
    return jsonify(data), 204
else:
    data["message"] = "指定数据不存在"
    return jsonify(data)
```

patch:

```
elif request.method == "PATCH":
    password = request.form.get("password")
    user = User.query.get(id)
    user.u_password = generate_password(password)

    data = {
    "messgage": "update success"
    }

    db.session.add(user)
    db.session.commit()

    return jsonify(data), 201
```





```python
# rest
# 视图函数可不可以返回json
@blue.route('/testJson/')
def testJson():
    data = {
        'msg':'ok',
        'status':200
    }
    print(type(data))
    # <class 'dict'>
    data = jsonify(data)
    print(type(data))
    <class 'flask.wrappers.Response'>
    return data

@blue.route('/toGetAnimal/')
def toGetAnimal():
    return render_template('getAnimal.html')
# 前后端分离源码的时候 是不可以直接传输对象的

# 查询
@blue.route('/getAnimal/')
def getAnimal():
    # animal = Animal.query.first()
    animal_list = Animal.query.all()

    animals = []

    for animal in animal_list:
        animals.append(animal.to_dict())

    data = {
        'msg':'ok',
        'status':200,
        'animals':animals
    }
    # return data
    return jsonify(data)


# 添加
@blue.route('/toRegister/')
def toRegister():
    return render_template('register.html')

@blue.route('/register/')
def register():
    name = request.args.get('name')

    animal = Animal()
    animal.name=name

    db.session.add(animal)
    db.session.commit()

    data = {
        'msg':'ok',
        'status':200,
        'animal':animal.to_dict()
    }

    return jsonify(data)

@blue.route('/index/')
def index():
    return '精神一点，下课去买雪糕'

# 修改
# put patch 有什么区别？  put 是修改全部  patch修改的是部分数据

@blue.route('/testPut/',methods=['put','patch'])
def testPut():
    animal = Animal.query.first()

    animal.name = 'python1'

    db.session.add(animal)
    db.session.commit()

    data = {
        'msg':'ok',
        'status':200
    }

    return jsonify(data)


# 删除
@blue.route('/testDelete/',methods=['delete'])
def testDelete():
    animal = Animal.query.first()

    db.session.delete(animal)
    db.session.commit()

    data = {
        'msg': 'ok',
        'status': 200
    }

    return jsonify(data)

# 或者 增删改查写在一个方法里,methods列表的请求方法必须大写
@blue.route('/animal/',methods = ['get','post','put','patch','delete'])
def animal():
    if request.method == 'GET':
        data = {
            'msg': 'get',
            'status': 200
        }

        return jsonify(data)

    elif request.method == 'POST':
        data = {
            'msg': 'post',
            'status': 200
        }

        return jsonify(data)

    elif request.method == 'PUT':

        data = {
            'msg': 'put',
            'status': 200
        }

        return jsonify(data)

    elif request.method == 'PATCH':
        data = {
            'msg': 'patch',
            'status': 200
        }

        return jsonify(data)

    elif request.method == 'DELETE':
        data = {
            'msg': 'delete',
            'status': 200
        }

        return jsonify(data)
```



## 十、flask-restful 框架简化开发

### 使用

```tex
（1）安装 
	pip install flask-restful

（2）初始化 
    在APP包下创建urls.py文件
    1.api = Api()
    2.def init_urls(app):
          api.init_app(app=app)
      注意：在__init__.py中调用init_urls
    3.api.add_resource(CatResouce, "/cat/")
      注意：CatResouce是一个类的名字，cat是路由，一定要写在def方法外。

（3）apis--基本用法
    在App包下创建apis文件夹
    1.在apis文件夹中创建 
    	模型名+Apis.py 的文件,继承自Resource。
    2.实现请求方法对应函数
    	class 模型Resource(Resource):
            def get(self):
                return {"msg": "ok"}
            def post(self):
                return {"msg": "create success"}

（4）乱码问题：init中  app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
```

```python
# =============urls.py================
from flask_restful import Api

from App.apis.Cat1Apis import Cat1Resource
from App.apis.Cat2Apis import Cat2Resource
from App.apis.CatApis import CatResource

api = Api()

def init_urls(app):
    api.init_app(app=app)

api.add_resource(CatResource,'/cat/')
```



```python
# CatApis.py
from flask_restful import Resource

class CatResource(Resource):
    def get(self):
        data = {
            'msg':'get',
            'status':200
        }
        return data

    def post(self):
        data = {
            'msg': 'post',
            'status': 200
        }
        return data

    def put(self):
        data = {
            'msg': 'put',
            'status': 200
        }
        return data

    def patch(self):
        data = {
            'msg': 'patch',
            'status': 200
        }
        return data

    def delete(self):
        data = {
            'msg': 'delete',
            'status': 200
        }
        return data
```

### 定制输入输出

#### (1)结构化输出：按照指定的格式输出

```python
1.@marshal_with()基本使用1
# ===============Cat1Apis.py==============
from flask_restful import Resource, marshal_with, fields

class Cat1Resource(Resource):
    r1Fileds = {
        'msg':fields.String,
        'status':fields.Integer,
        'error':fields.String(default='false'),
        'msg1':fields.String(attribute='a')
    }
    @marshal_with(r1Fileds)
    def get(self):
        data = {
            # 'msg':'ok',
            'status':200,
            'a':'b',
        }
        return data
总结：(1)默认返回的数据如果在预定义结构中不存在，数据会被自动过滤
	 (2)如果返回的数据在预定义的结构中存在，数据会正常返回
	 (3)如果返回的数据比预定义结构中的字段少，预定义的字段会呈现一个默认值
        如果类型是Integer  那么默认值是  0
        如果类型是String   那么默认值是null
 	 (4)fields后面的类型 可以加（） 可以不加（）
```

```tex
说明：
1. fields中的类型约束
（1）String
（2）Integer
（3）Nested    嵌套
（4）List
2. fields的约束
（1）attribute(指定连接对应名字)
	attribute=名字
（2）default(设置默认值)
    default=404
```

```python
2.@marshal_with()基本使用2
# ==========Cat2Apis.py============
from flask_restful import Resource, fields, marshal
r1Fields={
        'msg':fields.String()
  }

class Cat2Resource(Resource):
    def get(self):
        data = {
            'msg':'ok'
        }
        return  marshal(data=data,fields=r1Fields)
```



```python
3.@marshal_with返回一个类对象
案例：
# =========Cat3Apis.py=============
catfields = {
    'id':fields.Integer,
    'name':fields.String,
    'color':fields.String
}

r1fields = {
    'msg':fields.String,
    'cat':fields.Nested(catfields)
}

class CatResource(Resource):
    @marshal_with(r1fields)
    def get(self):
        cat = Cat.query.first()
        data = {
            'msg':'ok',
            'cat':cat
        }
        return data
```

```python
4.@marshal_with返回一个列表
案例：	
# ==========Cat4Apis.py==================
catfields = {
    'id':fields.Integer,
    'name':fields.String,
    'color':fields.String,
}

r1fields = {
    'msg':fields.String,
    'cats':fields.List(fields.Nested(catfields))
}

class CatResource(Resource):
    def get(self):
        cats = Cat.query.all()
        data = {
            'msg':'ok',
            'cats':cats
        }

        return marshal(data=data,fields=r1fields)
```

#### (2)结构化输入

```tex
1.使用步骤：  
在Class类外
（1）parser=reqparse.RequestParser()
（2）parser.add_argument("c_name", type=str,required=True, help="c_name必须填写"）	
parser.add_argument(name="id", type=int, required=True, help="id必须填写")
在Class类里
（3）parse = parser.parse_args()

（4）name = parse.get("name")
id = parse.get("id")
print(name,id)
         	 
总结: 
    name 		获取请求的参数名字
    type 		请求参数的类型
    required     必须填写
    help         如果没有填写报错  
```

```python
# ===========Cat5Apis.py===============
from flask_restful import Resource, reqparse

parser=reqparse.RequestParser()
# name 是要接受那个参数 type代表的是参数类型 required=True是不是必须填写   help如果没有添加那么他的默认参数
name=parser.add_argument("name", type=str, required=True, help="name不能为空")
age=parser.add_argument(name="id", type=int, required=True, help="id不能为空")


class Cat5Resource(Resource):

    def get(self):
        # name = request.args.get('name')
        # print('name')
        
        # 获取请求参数
        parse = parse.parse_args()
        name = parse.get('name')
        print(name)
        return {'msg':'ok'}

    def post(self):
        # age = request.form.get('age')
        # print(age)
        parse = parse.parse_args()
        age = parse.get('age')
        print(age)
        
        return {'msg': 'ok'}
```





```python
# ============urls.py====================
from flask_restful import Api

from App.apis.Cat1Apis import Cat1Resource
from App.apis.Cat2Apis import Cat2Resource
from App.apis.Cat3Apis import Cat3Resource
from App.apis.Cat4Apis import Cat4Resource
from App.apis.CatApis import CatResource

api = Api()


def init_urls(app):
    api.init_app(app=app)


api.add_resource(CatResource,'/cat/')
api.add_resource(Cat1Resource,'/cat1/')
api.add_resource(Cat2Resource,'/cat2/')
api.add_resource(Cat3Resource,'/cat3/')
api.add_resource(Cat4Resource,'/cat4/')
api.add_resource(Cat5Resource,'/cat5/')
```

```tex
# 项目结构
App
├── apis
    ├── Cat1Apis.py
    ├── Cat2Apis.py
    ├── Cat3Apis.py
    ├── Cat4Apis.py
    ├── Cat5Apis.py
    ├── CatApis.py
```

