## 一、Template概念

```tex
1 概念：在Django框架中，模板是可以帮助开发者快速生成，呈现给用户页面的工具。
2 模板的设计方式实现了MVT中的解耦，VT有着N:M的关系，一个V可以调用任意T，一个T可以供任意V使用。
3 模板处理分为两个进程
	（1）加载
	（2）渲染
4 模板中的动态代码段除了做基本的静态填充，可以实现一些基本的运算，转换和逻辑。
5 早期的web服务器  只能处理静态资源请求  模板能处理动态资源请求 依据计算能生成相应的页面。
6 注意：在Django中使用的就是Django模板，在flask种使用得是jinja2模板。
```

```tex
模板组成：主要有两部分
	1 HTML静态页码
	2 动态插入的代码块(挖坑，填坑)
```

## 二、模板语法

### 1、变量

```tex
变量:视图传递给模板的数据
	获取视图函数传递的数据使用{{ var }}接收
遵守标识符规则：
	拒绝关键字 保留字 数字。。。如果变量不存在，则插入空字符串
来源：
    视图函数中传递过来的
    标签中，逻辑创建出来的
```

### 2、模板中的点语法

```python
# 属性或者方法:
class Student(models.Model):
    s_name = models.CharField(max_length=16)
    def get_name(self):
        return self.s_name
# 弊端：模板中的小弊端，调用对象的方法，不能传递参数; 
# 为什么不能传递参数 ，因为连括号都没有,无法用括号来调用。
1 属性  student.name
2 方法  student.getName
3 索引  students.0.g_name
4 字典  student_dict.hobby
```

```python
def testPoint(request):
    dog = Dog.objects.first()
    dog_list = Dog.objects.all()
    dog_dict = {
        'sex':'x'
    }

    context = {
        'dog':dog,
        'dog_list':dog_list,
        'dog_dict':dog_dict
    }

    return render(request,'testPoint.html',context=context)
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    算今天还有6天 就回家了
    <hr>
    {{ dog.d_name }}
    <hr>
    {{ dog.getName }
    <hr>
    {{ dog_list.1.d_name }}
    <hr>
    {{ dog_dict.sex }}
</body>
</html>
```

### 3、标签

```tex
特征：标签分为单标签和双标签，双标签必须闭合。
```

```tex
功能标签：（for）
for
	for i in xxx
	1.empty
		判断之前的代码有没有数据 如果没有,显示empty下面的代码
		eg: {% for 变量 in 列表 %}
                语句1 
                {% empty %}
            	语句2
            {% endfor %}
    2.forloop
        循环状态的记录
        {{ forloop.counter }} 表示当前是第几次循环，从1数
        {{ forloop.counter0}}表示当前是第几次循环，从0数
        {{ forloop.revcounter}}表示当前是第几次循环，倒着数，到1停
        {{ forloop.revcounter0}}表示当前第几次循环，倒着数，到0停
        {{ forloop.first }} 是否是第一个  布尔值
        {{ forloop.last }} 是否是最后一个 布尔值
```

```tex
功能标签：（if）
if
    分支
    判断
    if - else
    if - elif -else
```

```tex
注释：
单行注释
	{#  被注释掉的内容  #}
多行注释
    {% comment %}
    	内容
    {% endcomment %}
```

```tex
乘法：widthratio
	{% widthratio 数  分母  分子  %}
	{% widthratio count 1 5 %}
	{% widthratio count 5 1 %}
```

```python
整除：{% if num | divisibleby:2 %}
		表格：奇偶行变色
		{% if forloop.counter|divisibleby:2 %}
```

```tex
ifequal： 
        ifequal
            {%  ifequal  value1 value2 %}
                语句
        	{% endifequal %}
            {% ifequal forloop.counter 5 %}
```

### 4、过滤器

```tex
| 管道符
将前面的输出作为后面的输出
1.add：
    <h4>{{ num|add:2 }}</h4>  加法
    <h4>{{ num|add:-2 }}</h4> 减法
2.upper：大写
3.lower：小写
4.safe 让标签生效
    确认安装
    进行渲染
------------------------------------
code = """
    <h2>睡着了</h2>
    <script type="text/javascript">
        var lis = document.getElementsByTagName("li");

        for (var i=0; i< lis.length; i++){
            var li = lis[i];
            li.innerHTML="日本是中国领土的一部分!";
        }
    </script>
"""
5.autoescape：让标签生效
    {% autoescape off %}
    code
    {% endautoescape %}
```

### 5、结构标签

```tex
1.block
    块
    坑
    用来规划页面布局，填充页面
    首次出现代表规划
    第二次c出现代表填坑
    第三次出现也代表填坑，默认会覆盖
    第N次...
    如果不想被覆盖  block.super
2.extends
    继承
    面向对象的体现
    提高模板的复用率
3.include
    包含
    将其它模板作为一部分，包裹到我们的页面中
```

### 6、加载静态资源

```tex
static-->包含 html  css js  img font
不推荐硬编码：静态资源路径 /static/css/xxx.css

需要在settings中添加  STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
推荐
    {% load static %}
    {% static 'xxx.css' %}
    
思考：html和模板中的页面  都可以使用load吗？  注意必须在模板中使用
坑点：仅在DEBUG模式下可以使用  如果settings中的DEBUG=False 那么是不可以使用的
```

```html
{% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
{#    <link rel="stylesheet" href="/static/getStatic.css">#}

    <link rel="stylesheet" href="{% static 'getStatic.css' %}">
</head>
<body>
    <ul>
        <li>洪世闲</li>
        <li>何书桓</li>
        <li>杨晨熙</li>
        <li>陈世美</li>
        <li>袁智敏</li>
    </ul>
</body>
</html>
```

## 三、常见的请求状态码

```tex
200 成功
301 永久重定向 302 重定向
403 防跨站攻击
404 路径错误  405 请求方式错误 
500 业务逻辑错误
```

## 四、视图函数

### 1、概念及基础语法

```tex
概念：视图函数MVT中的View，相当于MVC中Controller作用，控制器用来接收用户输入（请求），协调模板模型，对数据进行处理，负责的模型和模板的数据交互。
视图函数返回值类型（大方向）：
	1.以Json数据 形式返回
		前后端分离
		return JsonResponse
	2.以网页形式返回
		HttpResponse
		render
		redirect
		重定向到另一个网页
		错误视图(40x,50x)
```

```tex
url匹配正则注意事项:  
1.正则匹配时从上到下进行遍历，匹配到就不会继续向后查找了
2.匹配的正则前方不需要加反斜线
3.最好结尾加一个 /
4.正则前需要加 （r）表示字符串不转义
5.url匹配规则：按照书写顺序，从上到下匹配，没有最优匹配的概念，匹配到就停止了			
eg：
url(r'^hehe')
url(r'^hehehe')
当访问 127.0.0.1:8000/hehehe 时只会匹配到 hehe对应路由的视图函数而跳转不到 hehehe,所以最好结尾加一个 /
```

```
url接受参数：
2.如果需要从url中获取一个值，需要对正则加小括号
    url(r'^grade/(\d+)$',views.getStudents)
    注意，url匹配中添加了 () 取参，在请求调用的函数中必须接收一个参数	
    如：def  getStudents(request,classId)：
   
2.如果需要获取url路径中的多个参数，那就添加多个括号，默认按照顺序匹配路径名字
    url(r'^news/(\d{4})/(\d)+/(\d+)$',views.getNews),
    匹配年月日多个参数 
    eg:
    	def get_time(request,hour, minute, second):
    	return HttpResponse("Time %s: %s: %s" %(hour, minute, second))
    	
3.参数也可以使用关键字参数
    url(r'^news/(?P<year>\d{4})/(?P<month>\d)+/(?P<day>\d+)$',views.getNews),
    多个参数并且指定位置
    eg:
        def get_date(request,  month, day, year):
        return HttpResponse("Date %s- %s- %s" %(year, month, day))
------------------------------------
总结路径参数：
1.位置参数
    eg：
        127.0.0.1：8000/vie/testRoute/1/2/3/
        r('^testRoute/(\d+)/(\d+)/(\d+)/')
    使用圆括号包含规则
    一个圆括号代表一个参数
    代表视图函数上的一个参数
    参数个数和视图函数上的参数一一对应（除默认request）
2.关键字参数
    可以在圆括号指定参数名字 （?P<name>reg）
    视图函数中存在和圆括号中name对应的参数
    参数不区分顺序
    个数也需要保持一致，一一对应
```

### 2、内置函数

```tex
locals()
		将局部变量，使用字典的形式打包
		key是变量的名字
		value是变量的值
```

### 3、反向解析

```tex
反向解析的用处：获取请求资源路径，避免硬编码。
配置
(1)在根路由urls中
    url(r'^views/',include('ViewsLearn.urls',namespace='view'))在根路由中的inclue方法中添加namespace参数
(2)在子路由urls中
	url(r'^hello/(\d+)',views.hello,name='sayhello'),
	在子路由中添加name参数
(3)在模板中
	<a href="{% url 'view:sayhello' %}">Hello</a>
	调用的时候 反向解析的路径不能有编译错误  格式是  {% url 'namespace:name%}'

    如果存在位置参数
    	{% url  ‘namespace:name'   value1 value2 ... %}
    如果存在关键字参数
    	{% url 'namespace:name'   key1=value1 key2=vaue2 ...%}
    在模板中使用
    	<a href="{% url 'view:sayhello'  year=2017 %}">Hello</a>
优点：
如果在视图，模板中使用硬编码连接，在url配置发生改变时，需要变更的代码会非常多，这样导致我们的代码结构不是很容易维护，使用反向解析可以提高我们代码的扩展性和可维护性。
```

