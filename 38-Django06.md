## 一、模型继承

```tex
1.默认一个模型在数据库中映射一张表
如果模型存在继承的时候，父模型产生表映射
子模型对应的表会通过外键和父表产生关联
从表外键引用主表的主键
	不能说从表外键引用主表得主键就一定是模型继承 因为一对一 一对多 都会引用主表得主键
2.关系型数据库性能
	数据量越大性能越低
	关系越多越复杂越低性能越低
```

```python
抽象模型
	在父类的Model的元信息中添加  abstract=True
		class Meta:
      		abstract=True
	抽象的模型不会在数据库中产生表(如：Animal)
	子模型拥有父模型中的所有字段(如：a_name字段)
	class Animal(models.Model):
    	a_name = models.CharField(max_length=16)
    	class Meta:
            db_table = 'animal'
        	abstract = True
        	
	class Cat(Animal):
    	c_eat = models.CharField(max_length=32)

	class Dog(Animal):
    	d_legs = models.IntegerField(default=4)
```

## 二、静态资源

```python
1.静态资源和模板得区别
（1）模板的路径不可以直接访问  必须通过http请求来访问
	static资源可以直接访问
（2）模板的语法不可以在静态资源中书写
2.注意：
（1）使用的时候注意配置资源位置
在settings.py中配置
	STATICFILE_DIRS=[os.path.join(BASE_DIR,'static')]
在模板中使用  
	{% load static %}
	{% static '相对路径' %}
（2）全栈工程师   要求会templates
　　　开发工程师   前后端分离static
```

## 三、文件上传

```
要求：客户端
	必须使用POST请求
	指定form表单中　enctype='multiplepart/form-data'
```

```python
原生代码：适用django也适用于flask
	1.从 request.FILES 中获取到上传上来的文件
	2.打开一个文件，从上传上来的文件进行读取，向打开的文件中进行写入，必须以二进制的格式来书写
	3.每次写入记得 flush 冲刷
比如：读取一个 13k的文件,每次读取 5k最后的 3k利用冲刷强制读取
# ---------------------------------------	
def upload_file(request):
	if request.method == "GET":
    	return render(request, 'upload.html')
	elif request.method == "POST":
		icon = request.FILES.get("icon")
		print(type(icon))
		with open("/home/xxx/static/img/icon.jpg", 'wb') as fp:
            # /static/img/icon.jpg 该文件夹是自己手动创建的
			for context in icon.chunks():
				fp.write(context)
				fp.flush()
                fp.close()
		return HttpResponse("文件上传成功")
 # ---------------------------------------       
 实现步骤：
（1）表单得请求方式是post
（2）添加表单得属性 enctype='multipart/form-data'  二进制传输
（3）input得type属性值为file
（4）获取表单中得file值  request.FILES.get获取的是文件的名字
（5）with open打开一个路径，然后以wb的模式使用
    for i in xxx.chunks()
        fp.write()
        fp.flush()
        fp.close()
```

```python
Django内置：
（1）创建模型并且指定ImageField属性（注意依赖于pillow，pip install pillow）
        例如：u_icon = models.ImageField(upload_to='icons')
        imageField在数据库中的数据类型是varchar,默认长度为100
（2）settings中指定 MEDIA_ROOT
    MEDIA_ROOT = os.path.join(BASE_DIR, 'static/upload')
    注意：media_root后面的数据类型不是一个列表
        会自动的创建文件夹
        该文件夹的路径是MEDIA_ROOT + ImageField的upload_to的值
注意：
	1：重复添加同一个图片，那么会直接添加进去，文件的名字是文件名原名+唯一串
	2：数据库icon的值是　upload_to + 文件名字
		
	隐藏bug：linux系统下文件夹的第一级子目录下 最多存储65535个文件
	解决方法：按时间来存储文件夹
		u_icon = models.ImageField(upload_to='%Y/%m/%d/icons')
		支持时间格式化
			%Y
			%m
			%d
			%H
			...
			专门用来解决linux的bug的   文件夹的第一级子目录下 最多存储65535个文件
# -------------------------------------------
案例：
@csrf_exempt
def image_field(request):
    if request.method == "GET":
        return render(request, 'image_field.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        icon = request.FILES.get("icon")
        user = UserModel()
        user.u_name = username
        user.u_icon = icon
        user.save()
        return HttpResponse("上传成功%d" % user.id)
模型：
class UserModel(models.Model):
	name = models.CharField(max_length=64)
	#ImageField依赖Pillow库 所以需要安装  pip install pillow
	#upload_to 依赖MEDIA_ROOT
	icon = models.ImageField(upload_to='%Y/%m/%d/icons')
# ------------------------------------------                 
实现步骤：
（1）表单的提交方式必须是post
（2）添加表单的属性enctype = mutipart/form-data
（3）在settings中设置MEDIA_ROOT = os.path.join(BASE_DIR,'XXX')
（4）创建模型  模型的属性是imagefield 
（5）注意imagefield依赖于pillow
（6）imagefield的约束是upload_to 该属性值和MEDIA_ROOT会进行拼接
（7）实例化对象 然后save保存即可
```

```python
# 将数据库的文件读取出来　然后显示头像
def getImage(request):
    user = User.objects.last()
    icon = user.u_icon
    context = {
        # 'icon':'/static/uploadDjango/'+str(icon) # 注意icon要转化成字符串
        'icon':'/static/uploadDjango/'+icon.url
    }

    return render(request,'getImage.html',context=context)
```

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        img{
            width: 100px;
            height: 100px;
            border-radius: 50%;
        }

    </style>

</head>
<body>
{#硬编码#}
{#    <img src="/static/upload/xz.jpg" alt="">#}

{#load static#}
{#    <img src="{% static 'upload/xz.jpg' %}" alt="">#}

{#从数据库中读取数据 然后展示对应的头像#}
<img src="{{ icon }}" alt="">
</body>
</html>
```

## 四、缓存

```tex
1.目的：
	缓解服务器的读写压力
	提升服务器的响应速度
	提升用户体验
	将执行过的操作数据 存储下来，在一定时间内，再次获取数据的时候，直接从缓存中获取
	比较理想的方案，缓存使用内存级缓存
	Django内置缓存框架
	存储中间数据的一种介质
2.原则：
    较少的代码
    对缓存后端封装一致性操作
    有点类似于ORM的感觉
    可扩展性
    应该存在通用基类
```

### Django内置缓存实现（三种方案）

```python
1.使用系统封装的(和基于数据库的区别是:数据库中多出来一张Animal表)
	装饰器封装在视图函数上
		@cache_page(30)
		需要注意的是不需要写timeout
	模板中也可以缓存--django内置得数据库缓存
    # 例如：
		@cache_page(30)
		def testCache1(request):
			time.sleep(5)
			return HttpResponse('testCache1')
	    数据库缓存相对比较低效
```

```python
2.基于数据库：在真实的mysql数据库中去创建缓存表
（1）创建缓存表
		python manage.py createcachetable [table_name]
（2）settings中配置缓存信息
    实例：
    CACHES={
              'default':{
                  'BACKEND':'django.core.cache.backends.db.DatabaseCache',
                  'LOCATION':'my_cache_table',# 和上面创建的缓存表名相同
                  'TIMEOUT':60,# 缓存的时间以set方法为主
                  'KEY_PREFIX':'python190x',
              }
           }
```

```python
3.基于redis-内存级数据库
	Django-redis-cache:
		使用redis实现django-cache的扩展
		操作缓存的API没有发生任何变更
		变更的就是连接缓存的配置
	常见的有两个实现:
		# django-redis 
			http://django-redis-chs.readthedocs.io/zh_CN/latest/#django
			pip install django-redis
		# django-redis-cache
			https://pypi.python.org/pypi/django-redis-cache/
			pip install django-redis-cache
	基本配置settings.py:
		CACHES={
                    'redispython190x':{
                        'BACKEND':'django_redis.cache.RedisCache',
                        'LOCATION':'redis://127.0.0.1:6379/1',
                        'OPTIONS':{
                                'CLIENT_CLASS':'django_redis.client.DefaultClient'
                        }
                    }
                }
	查看redis缓存:
		select 1
		keys *
		get :1:news
		查看过期时间  tts  :1:news
```

```python
多缓存：
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
        'TIMEOUT': 60 * 5,
		'KEY_PREFIX':'python1905',
    },

    'redis_backend': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        'KEY_PREFIX':'redispython1905',
    }
}
	写多套配置，定义不同的名字
	存入缓存的时候，获取不同的缓存对象
	想使用哪个缓存就创建哪个缓存的实例对象
	
	装饰器实现多缓存
		@cache_page(30, cache='cache_name')
		可以使用装饰器 指定想要的数据库
	数据库实现多缓存
		 cache = caches['cache_name']
```

```python
@cache_page(30)
def testCache1(request):
    time.sleep(5)
    return HttpResponse('测试装饰器缓存')

def testCache2(request):
    value = cache.get('ip')
    if value:
        return HttpResponse(value)
    else:
        ip = request.META.get('REMOTE_ADDR')
        cache.set('ip',ip,timeout=10)
        return HttpResponse('测试数据库缓存')


def testCache3(request):
    value = cache.get('ip')
    if value:
        return HttpResponse(value)
    else:
        ip = request.META.get('REMOTE_ADDR')
        cache.set('ip',ip)
        return HttpResponse('测试内存级数据库缓存')
# 多缓存
@cache_page(30,cache='redis_backend')
def testCache4(request):
    time.sleep(3)
    return HttpResponse('装饰器实现多级缓存')

def testCache5(request):
    cache = caches['default']
    value = cache.get('ip')
    if value:
        return HttpResponse(value)
    else:
        ip = request.META.get('REMOTE_ADDR')
        cache.set('ip',ip)

        return HttpResponse('数据库实现多缓存')
```



## 五、中间件

```
中间件：是一个轻量级的，底层的插件，可以介入到Django的请求和响应过程（面向切面编程）
中间件的本质就是一个python类
面向切面编程（Aspect Oriented Programming）简称AOP。AOP的主要实现目的是针对业务处理过程中的切面进行提取，它所面对的是处理过程中的某个步骤或阶段，以获得逻辑过程中各部分之间低耦合的隔离效果。
```

![](/media/xcw/5000476200474DE2/迅雷下载/第二阶段资料/0930/doc/media/aop.png)

```
django内置的一个底层插件
从属于面向切面编程AOP
	在不修改源代码的情况下，动态去添加一些业务逻辑处理
中间件的典型实现 装饰器
	中间件就是使用类装饰实现的
```

```tex
面向切面编程
切点
（1）process_request
	process_request(self,request):在执行视图前被调用，每个请求上都会调用，不主动进行返回或返回HttpResponse对象

（2）process_view
	process_view(self,request,view_func,view_args,view_kwargs)：调用视图之前执行，每个请求都会调用，不主动进行返回或返回HttpResponse对象

（3）process_template_response	
	process_template_response(self,request,response):在视图刚好执行完后进行调用，每个请求都会调用，不主动进行返回或返回HttpResponse对象

（4）process_response
	process_response(self,request,response):所有响应返回浏览器之前调用，每个请求都会调用，不主动进行返回或返回HttpResponse对象

（5）process_exception
	process_exception(self,request,exception):当视图抛出异常时调用，不主动进行返回或返回HttpResponse对象

切面
切点处切开可以获得的数据
```

```python
实现步骤：
书写，自定义中间件
1. 在工程目录下创建middleware目录
2. 目录中创建一个python文件
3. 在python文件中导入中间件的基类
	from django.utils.deprecation import MiddlewareMixin
4. 在类中根据功能需求，创建切入需求类，重写切入点方法
    class LearnAOP(MiddlewareMixin):
        def process_request(self,request):
            print('request的路径',request.GET.path)
5. 启用中间件，在settings中进行配置，MIDDLEWARE中添加
middleware.文件名.类名
```

```python
应用：
def get_phone(request):
	if random.randrange(100) > 95:
		return HttpResponse("恭喜你抢到了小米8")
	return HttpResponse("正在排队")
1.白名单
class ConnAOP(MiddlewareMixin):
    def process_request(self,request):
        if request.path == "/app/getphone/":
            if ip == "127.0.0.1":
                if random.randrange(100) > 20:
                    return HttpResponse("恭喜您免费获取小米8 256G版")
2.黑名单
if request.path == "/app/getticket/":
	if ip.startswith("10.0.122.1"):
		return HttpResponse("已抢光")
作业：如果一分钟之内访问了10次 那么返回 小爬虫快走开，如果1分钟之内访问了30次 封ip 5分钟  正常访问 返回来了老弟
```

```python
当某一段业务逻辑发生了错误  那么就会执行process_exception方法
	界面友好化 应用交互友好化
	def process_exception(self, request, exception):
	        print(request, exception)
	        return redirect(reverse('app:index'))
```

```
注意：中间件的执行顺序
	 中间件注册的时候是一个列表
	 如果我们没有在切点处直接进行返回，中间件会依次执行
	 如果我们直接进行了返回，后续中间件就不再执行了
```

```python
#--------urls.py---------
# 小米
url(r'^getPhone/',views.getPhone),

# process_exception
# 中间件可以有返回值 也可以没有返回值
# 当中间件有返回值的时候  那么是不会在执行视图函数了

# process_exception的作用是在执行视图函数中 如果有错误了 那么就执行peocess_exception
url(r'^testException/',views.testException),
# -------views.py---------
def getPhone(request):
    if random.randrange(100) > 80:
        return HttpResponse('恭喜抢到了小米2手机')
    else:
        return HttpResponse('哪凉快哪眯着去')

def testException(request):
    a = 1
    b = 0
    c = a / b
    print(c)

    return HttpResponse('testException')
# -------middleware.py--------
class ConnAOP(MiddlewareMixin):
    def process_request(self,request):
        # print('莫雷你个sb')
        # print('链接数据库')

        # 白名单
        # ip = request.META.get('REMOTE_ADDR')
        #
        # if ip == '127.0.0.1':
        #     if random.randrange(100) > 40:
        #         return HttpResponse('恭喜你抢到了')


        # 黑名单
        # ip = request.META.get('REMOTE_ADDR')
        #
        # if ip == '127.0.0.1':
        #     pass
            # return HttpResponse('已经抢光')

        print('听说国外记者专门拍摄阅兵时候士兵眨眼睛')
        # return HttpResponse('外交风云')

class ExceptionAOP(MiddlewareMixin):
    # def process_exception(self,request,exception):
    #
    #     return redirect(reverse('midd:index'))

    def process_request(self,request):
        print('我们不眨眼')
```



## 六、分页器 

```
分页是了提升用户体验，并且减小服务器的负担而开发的
分页：
    真分页   每一次点击下一页或者上一页 都会像数据库发送请求 并且返回数据
    假分页   一次性读取所有数据  然后再内存中进行分页
    企业级开发中常用 真分页   
```

```
原生实现
	偏移加限制
	offset  limit
	students = Student.objects.all()[per_page*(page-1): page * per_page]
```

```python
封装实现
	Paginator（分页工具）
		对象创建
			Paginator(数据集，每一页数据数)
			例如：paginator = Paginator(students, per_page)
		属性
			count对象总数
			num_pages：页面总数
			page_range: 页码列表，从1开始
		方法:
			page(整数): 获得一个page对象
				       该方法的返回值类型是Page
		常见错误:
			InvalidPage：page()传递无效页码
			PageNotAnInteger：page()传递的不是整数
			Empty：page()传递的值有效，但是没有数据
	Page（具体哪一页）
		对象获得
			通过Paginator的page()方法获得
			例如：student=paginator.page(1)
		属性
			object_list：	当前页面上所有的数据对象
			number：	当前页的页码值
			paginator:	当前page关联的Paginator对象
		方法
			has_next()	:判断是否有下一页
			has_previous():判断是否有上一页
			has_other_pages():判断是否有上一页或下一页
			next_page_number():返回下一页的页码
			previous_page_number():返回上一页的页码
			len()：返回当前页的数据的个数
			
			
应用场景：paginator对象  适用于 页码的遍历  eg：上一页 1 2 3  下一页
         page对象       适用于 是否有上一页 下一页  上一页页码  下一页页码 
```

```python
def getPage(request):
    page = int(request.GET.get('page',1))
    per_page = int(request.GET.get('per_page',2))

    # animal_list = Animal.objects.all()[0,2]
    # animal_list = Animal.objects.all()[2,4]
    # animal_list = Animal.objects.all()[4,6]
    animal_list = Animal.objects.all()[(page-1)*per_page,page*per_page]
    for animal in animal_list:
        print(animal.id,animal.a_name,animal.a_color)
    return HttpResponse('查询成功')

# page和per_page不需要做强制类型转换
def getPageDjango(request):
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 2)
    animal_list = Animal.objects.all()
    pagin = Paginator(animal_list,per_page)
    p = pagin.page(page)
    context={
        'p':p,
        'pagin':pagin,
        'page':int(page),
    }
    return render(request,'getPageDjango.html',context=context)
```

```html
<!--getPageDjango.html-->
<ul>
    {% for foo in p.object_list %}
        <li>{{ foo.id }}:::{{ foo.a_name }}:::{{ foo.a_color }}</li>
    {% endfor %}
</ul>
    {% if p.has_previous %}
        <a href="{% url 'page:getPageDjango' %}?page={{ p.previous_page_number }}">上一页</a>
        {% else %}
        <a href="#">上一页</a>
    {% endif %}

    {% for foo in pagin.page_range %}
        {% if foo == page %}
            <a style="color: green" href="{% url 'page:getPageDjango' %}?page={{ foo }}">{{ foo }}</a>
            {% else %}
            <a href="{% url 'page:getPageDjango' %}?page={{ foo }}">{{ foo }}</a>

        {% endif %}
    {% endfor %}

    {% if p.has_next %}
        <a href="{% url 'page:getPageDjango' %}?page={{ p.next_page_number }}">下一页</a>
        {% else %}
        <a href="#">下一页</a>
    {% endif %}
```



## 七、富文本

```python
富文本:Rich Text Format（RTF），是有微软开发的跨平台文档格式，大多数的文字处理软件都能读取和保存RTF文档，其实就是可以添加样式的文档，和HTML有很多相似的地方。
	写论坛，博客时使用的一种带样式的文本插件
插件使用方式：
（1）安装插件
	pip install django-tinymce
（2）在INSTALLED_APP中添加 tinymce
（3）初始化
    在settings中注册tinymce应用
    设置默认的配置文件
    TINYMCE_DEFAULT_CONFIG = {
        'theme':'advanced',
        'width':800,
        'height':600,
    }
（4）创建模型
    from tinymce.models import HTMLField
    class Blog(models.Model):
        sBlog = HTMLField()
（5）在页面中使用
    文本域: <textarea></textarea>
    引入tinymce:
    <script type="text/javascript" src="/static/tiny_mce/tiny_mce.js"></script>
    初始化绑定文本域:
    <script type="text/javascript">
    tinyMCE.init({
        "mode": "textareas",
        "theme": "advanced",
        "width": 800,
        "height": 600
    })
    </script>
```

```python
@csrf_exempt
def testRTF(request):
    if request.method == 'GET':
        return render(request,'testblog.html')

    elif request.method == 'POST':
        sblog = request.POST.get('blog')

        blog = Blog()
        blog.sBlog = sblog
        blog.save()
        return HttpResponse('添加博客成功')
```

## 八、thefuck

```tex
thefuck:一个终端指令修复工具
当指令在输入错误的时候，我们可以通过fuck进行弥补
可以提供指令修复方案:
    enter
    	确定
    control+c
    	取消
    ↑↓ 
    	调整
使用:
（1）sudo apt update
（2）sudo apt install python3-dev python3-pip
（3）sudo pip3 install thefuck
（4）更新环境变量
    vim ~/.bashrc
    eval "$(thefuck --alias fuck)"
    source ~/.bashrc
```

