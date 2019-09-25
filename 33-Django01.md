```tex
1.创建虚拟环境
2.安装Django
	pip install django==1.11.7
3.创建Django项目
	django-admin startproject xxx
4.启动服务器的命令
	python manage.py runserver
5.项目的结构 tree
----------------------------
	项目名字
		项目名字
			__init__
			urls
			settings
			wsgi
		manage.py
-----------------------------
例如：HelloDjango		
        ├──  HelloDjango
        │      ├── __init__.py
        │      ├── settings.py
        │      ├── urls.py
        │      └── wsgi.py
        ├── manage.py
------------------------------
6.修改Pycharm的虚拟环境步骤
	file-->settings-->project interpreter-->add-
	-->existing envrinment-->...虚拟环境文件夹-->
	bin-->python
7 修改欢迎页面为中文
    在settings中修改LANGUAGE_CODE = 'zh-hans'

8 修改为当前系统时间
    在settings中修改TIME_ZONE = 'Asia/Shanghai'

9 允许所有主机访问
    在settings中修改ALLOWED_HOSTS = ['*']
    允许访问的主机  '*'代表所有人都可以访问

10 启动服务器设置端口号和主机
    python manage.py runserver
    python manage.py runserver 8888
    python manage.py runserver 0.0.0.0:9000
	注意:主机名必须和端口号成对出现
11 视图函数的位置
    （1）项目名字下的视图函数  基本不用
            在urls定义路由路径
                url(r'^路径/',views.视图函数名字不加圆括号)
                    eg:url(r'^index/',views.index)
            在views中定义视图函数
                def index(request):
                    return HttpResponse('index')

     如果把所有的视图函数都放在项目下了 那么代码看起来就特别的臃肿
     所以我们一般的企业级开发 都是把每一个模块封装出一个app
    （2）App
            1.创建App
                 django-admin startapp App 
                 -----------------------------
                 python manage.py startapp App
            2.在App中创建urls
            3.在urls中创建urlpatterns=[ ] 我们称在app下urls叫做子路由
            4.在根路由（项目下的urls）加载子路由  url(r'^app/',include('App.urls'))
            5.在子路由中定义请求资源路径也就是路由
                url(r'^index/',views.index)
            6.在App下的views下创建视图函数
            7.访问 127.0.0.1：8000 / 根路由的名字/子路由的名字
              	例如:127.0.0.1:8000/app/index/

```

## 一、Django

### 简介

```tex
Django是一个开放源代码的Web应用框架，它最初是被开发来用于管理劳伦斯出版集团旗下的一些以新闻内容为主的网站的，即是CMS（内容管理系统）软件。并于2005年7月在BSD许可证下发布。这套框架是以比利时的吉普赛爵士吉他手Django Reinhardt来命名的。
	重量级，替开发者想了太多的事情，帮开发者做了很多的选择，内置了很多的功能。
	
官方网站
	http://www.djangoproject.com
使用版本1.11.7
	LTS：长期支持版本
	以后再学2.2 LTS
```

### 虚拟环境

```bash
mkdir django1905
cd django
virtualenv .env
source .env/bin/activate   
deactivate                 退出虚拟环境
```

### 虚拟化技术

```tex
1 虚拟机
2 虚拟容器
	Docker 支持多种语言
3 虚拟环境 -- 迷你
	python专用
	目的：将python依赖隔离
```

### 创建Django项目

```tex
1 django-admin startproduct 项目名字
	tree 命令观察项目结构
	如果未安装 sudo apt install tree
```

```tex
2 项目结构
	项目名字
		-manage.py
			管理整个项目的文件
			以后的命令基本都通过他来调用
		-项目名字
			__init__
				python包而不是一个文件夹
			settings
				项目全局配置文件
					ALLOWED_HOST=["*"]
					修改settings
						LANGUAGE_CODE='zh-hans'
						TIME_ZONE='Asia/Shanghai'
			urls
				根路由
					url（p1,p2）
			wsgi
				用在以后项目部署上，前期用不到
				服务器网关接口
				webserver gateway interface
 TestDjango
    ├── manage.py
    └── TestDjango
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

```tex
3 启动项目
	python manage.py runserver
		使用开发者服务器启动项目
		默认会运行在本机的 8000端口上
	启动服务器命令：
	(1)python manage.py runserver
	(2)python manage.py runserver 8888
	(3)python manage.py runserver 0.0.0.0:9000
```

```tex
4 创建一个应用
python manage.py startapp App
或者 django-admin startapp App
	App结构
		__init__
		views
			视图函数
			视图函数中参数是request，方法的返回值类型是HttpResponse
		models
			模型
		admin
			后台管理
		apps
			应用配置
		tests
			单元测试
		migrations
			__init__
			迁移目录
```

### 拆分路由

```tex
python manager.py startapp Two
创建urls:
	urlspatterns=[
		urls(r'^index',views.index)
	]
创建views方法
	主路由应用
		urls(r'^two/',include('Two.urls'))
	浏览器访问url
		127.0.0.1:8000/two/index
```

### 编写第一个请求

```tex
1.编写一个路由
      url(p1, p2)
           url(r'^index/',views.index),
      p1 正则匹配规则,p2 对应的视图函数
2.编写视图函数
	（1）本质上还是一个函数
		def index(request):
    		return HttpResponse('123')
		要求：只是默认第一个参数是一个request(类型是HttpRequest)，必须返回一个HttpResponse对象。
	（2）返回值：
		1.HttpResponse()
			HttpResponse('123')
			HttpResponse('<h1>123</h1>')
	    2.render
			在App下创建templates
		    注意:名字是固定的，不能打错单词.
			render方法的返回值类型也是一个HttpResponse类型的.
			要求：
				第一个参数是request，第二个参数的是页面
			---------------------------------------------
	        注意:需要在settings里的INSTALLED_APPS设置App路径
			将应用注册到项目的settings中INSTALLED_APPS中
            加载路由的方式:
                1--> INSTALLED_APPS---》'Two'
                2--> INSTALLED_APPS---》'Two.apps.TwoConfig'  版本限制 1.9之后才能使用
3.模板配置有两种情况
		(1)在App中进行模板配置
		  - 只需在App的根目录创建templates文件夹即可
		  - 必须在INSTALLED_APP下安装App
		(2)在项目目录中进行模板配置
		  - 需要在项目目录中创建templates文件夹并标记
		  - 需要在settings中进行注册  
         settings-->TEMPLATES-->DIRS-->	os.path.join(BASE_DIR,'templates')				 
		  注意：开发中常用项目目录下的模板    理由：模板可以继承，复用
```

### Django中的工作机制

```python
1.用python manage.py runserver 启动Django服务器时就载入了在同一目录下的settings.py。该文件包含了项目中的配置信息，如URLConf等，其中最重要的配置就ROOT_URLCONF，它告诉Django哪个Python模块应该用作本站的URLConf，默认的是urls.py。

2.当访问url的时候，Django会根据ROOT_URLCONF的设置来装载URLConf。

3.然后按顺序逐个匹配URLConf里的URLpatterns。如果找到则会调用相关联的视图函数，并把HttpRequest对象作为第一个参数(通常是request)

4.最后该view函数负责返回一个HttpResponse对象。
```

