## 一、request对象

```tex
概念：django框架根据Http请求报文自动生成的一个对象，包含了请求各种信息。
属性：
1.path：请求的完整路径
2.method：GET  1.11版本最大数据量2K
		  POST  参数存在请求体中，文件上传等。
          请求的方法，常用GET,POST
          应用场景：前后端分离的底层 判断请求方式 执行对应的业务逻辑
4.GET：QueryDict类字典结构 key-value
       一个key可以对应多个值
       get 重复的变量，获取最后一个
       getlist 获取多个
       类似字典的参数，包含了get请求方式的所有参数
5.POST： 类似字典的参数，包含了post请求方式的所有参数
6.encoding：编码方式，常用utf-8
7.FILES：类似字典的参数，包含了上传的文件  文件上传的时候会使用  
        页面请求方式必须是post   
        form的属性enctype=multipart/form-data
        flask和django通用的   一个是专属于django
8.COOKIES：类似字典的参数，包含了上传的文件  获取cookie
9.session：类似字典，表示会话
10.META:应用反爬虫  最重要的：REMOTE_ADDR  拉入黑名单
        客户端的所有信息 ip
        print(request.META)
        for key in request.META:
            print(key, request.META.get(key))
            print("Remote IP", request.META.get("REMOTE_ADDR"))
```

```python

# 当遇到post请求的时候 那么会验证csrf  放跨站攻击  解决方法：注释settings中的中间件
def testRequest(request):
    # 请求资源路径
    # 应用场景： 判断某请求是否在某请求列表下
    #  REQUEST_LIST = ['/cart/']
    #  if request.path in REQUEST_LIST:
    print(request.path)

    # 获取请求方式
    print(request.method)

    # queryDict 和Dict的区别？
    # dict是字典对象，没有urlencode()方法；
    # QueryDict对象，有urlencode()方法，作用是将QueryDict对象转换为url字符串；
    # queryDict默认的value值是一个列表
    # dict的默认value值是一个字符串


    # 返回的结构<QueryDict: {'name': ['zs']}>
    #         <QueryDict: {'age': ['18'], 'name': ['zs']}>
    # django中获取get请求参数的方法
    print(request.GET.get('name'))
    # 如果是重复的变量  那么会接受后面的那个数据
    print(request.GET.get('age'))
    print(request.GET.getlist('age'))


    # django中获取post请求的参数
    print(request.POST)
    print(request.POST.get('name'))
    print(request.POST.getlist('age'))

    # 编码
    print(request.encoding)

    # 反扒
    print(request.META.get('REMOTE_ADDR'))

    for key in request.META:
        print(key,request.META.get(key))


    return HttpResponse('今天是个好日子')
```

## 二、HttpResponse对象

当浏览器访问服务器的时候  那么服务器响应的数据类型

响应分类：

（1）HTML响应   （2）JsonResponse（前后端分离） 

### 1、HTML响应

```python
1.基类HttpResponse   不使用模板，直接HttpResponse()
	def hello(request):
        response = HttpResponse()
        response.content = "德玛西亚"
        response.status_code = 404
        response.write("千锋")
        response.flush()
        return response
     方法
		 init				    初始化内容
	     write('文本')		   直接写出文本
         flush()				冲刷缓冲区
         set_cookie(key,value='xxx',max_age=None,exprise=None)
         delete_cookie(key)		删除cookie，上面那个是设置
         
2.render转发：
		方法的返回值类型也是一个HttpResponse

3.HttpResponseRedirect重定向
    HttpResponse的子类，响应重定向:可以实现服务器内部跳转
	return HttpResponseRedict('/grade/2017')使用的时候推荐使用反向解析
	
	状态码：302
	
	简写方式：简写redirect方法的返回值类型就是HttpResponseRedirect
	
	反向解析：
    （1）页面中的反向解析 url方法
        基本使用
        	{% url 'namespance:name' %}
        url 位置参数
        	{% url 'namespace:name'  value1 value2 %}
        url关键字参数
        	{% url 'namespace:name' key1=value1 key2 = value2 %}
    （2）python代码中的反向解析（一般python代码的反向解析都会结合重定向一起使用）
        基本使用
        	reverse('namespace:name')
        位置参数
            reverse('namespace:name', args=(value1, value2 ...))
            reverse('namespace:name', args=[value1, value2 ...])
        关键字参数
        	reverse('namespace:name', kwargs={key1:value2, key2:value2 ...})
```

```python
def testResponse(request):

    response = HttpResponse()

    response.content = '明天有相亲大会，下午开始'
    response.status_code = 405
    response.write('恭祝1905兄弟们相亲成功')

    # 字节流  字节缓冲流  字符流   字符缓冲流
    # 13kb   每次读取5字节
    response.flush()

    return response


def testRender(request):
    response = render(request,'testRender.html')
    print(type(response))
    return response

# HttpResponseRedirect 是HttpResponseRedirectBase的子类
# HttpResponseRedirectBase是HttpResponse的子类
# 状态码是302


# HttpResponsePermanentRedirect  永久重定向
# HttpResponsePermanentRedirect的父类是HttpResponseRedirectBase
# # HttpResponseRedirectBase是HttpResponse的子类
# 状态码是301
def testRedirect(request):
    return HttpResponseRedirect('/res/index/')

# redirect方法判断了permanent
#     if kwargs.pop('permanent', False):
#         redirect_class = HttpResponsePermanentRedirect
#     else:
#         redirect_class = HttpResponseRedirect
def testRedirect1(request):
    return redirect('/res/index/')


def index(request):
    return HttpResponse('欢迎光临珍爱网相亲大会')


# 增 删 改  查    按钮

# 增  redirect
# 删除 redirect
# 点击修改  执行的render  提交表单是redirect
# 查询  render

# 重定向     是一件事做完  去做另一件事 eg 添加 成功 之后 去查询
# 转发/渲染  一件事没有做完

# 转发和重写向的区别？
# 转发共享了request对象
# 重定向是执行了2次请求

# redirect（/res/index/）
# render(request,'index.html'，context=context)
# request.setxxx('context':context)
#  {{ }}  ===>request.getxxx('context')

def test(request):
    name = 'zs'
    return render(request,'test.html',context=locals())


def testReverse(request):
    return HttpResponse('专门用来测试python中反向解析的语句')


def testReverseBase(request):
    a = reverse('res:testReverse')
    # /res/testReverse/
    print(a)

    return redirect('/res/testReverse/')
    # return redirect(reverse('res:testReverse'))


def testReverseLocal(request,month,day,year):
    return HttpResponse(year + '/' + month + '/' + day)


def testLocal(request):
    return redirect(reverse('res:testReverseLocal',args=[2019,9,27]))


def testReverseKey(request,month,day,year):
    return HttpResponse(year + '/' + month + '/' + day)


def testKey(request):
    return redirect(reverse('res:testReverseKey',kwargs={'year':2019,'month':9,'day':27}))
```



### 2、JsonResponse

```
这个类是HttpRespon的子类，它主要和父类的区别在于：
1.它的默认Content-Type 被设置为： application/json

2.第一个参数，data应该是一个字典类型，当 safe 这个参数被设置为：False ,那data可以填入任何能被转换为JSON格式的对象，比如list, tuple, set。 默认的safe 参数是 True. 如果你传入的data数据类型不是字典类型，那么它就会抛出 TypeError的异常。

def get_info(request):
	data = {
        "status": 200,
        "msg": "ok",
    }
	return JsonResponse(data=data)
```

```python
# JsonResponse继承了HttpResponse
def testJson(request):

    data = {
        'msg':'ok',
        'status':200
    }

    return JsonResponse(data=data)

# ---------返回一个对象------------
def testJsonObject(request):
    animal = Animal.objects.last()

    data = {
        'msg':'ok',
        'status':200,
        'animal':animal.to_dict()
    }
    return JsonResponse(data=data,json_dumps_params={'ensure_ascii':False})

#----------返回一个列表-------------
def testJsonList(request):

    animal_list = Animal.objects.all()

    animals = []

    for animal in animal_list:
        animals.append(animal.to_dict())
    data = {
        'msg': 'ok',
        'status': 200,
        'animals': animals
    }
    return JsonResponse(data=data, json_dumps_params={'ensure_ascii': False})
													    # 乱码问题
```



### 3、HttpResponse子类

```
HttpResponseRedirect 
	-302
HttpResponsePermanentRedirect
    - 重定向，永久性- 
    -301
HttpResponseBadRequest	
	-400
HttpResponseNotFound
	- 404
HttpResponseForbidden
	- 403   csrf 防跨站攻击 
HttpResponseNotAllowed
	- 405   
HttpResponseServerError
	- 500
Http404- Exception
	- raise 主动抛异常出来
```

## 三、会话技术

```
为什么会有会话技术？
	服务器如何识别客户端
	Http在Web开发中基本都是短连接
	请求生命周期从Request开始，到Response就结束
会话技术：cookie session  token（自定义的session）
```

### 1、cookie：

```tex
1.概念	
	客户端会话技术，数据都存储在客户端，以key-value进行存储，支持过期时间max_age，默认请求会携带本网站的所有cookie，cookie不能跨域名，不能跨浏览器，cookie默认不支持中文base64
	
2.cookie是服务器端创建  保存在浏览器端
	设置cookie应该是服务器 response
	获取cookie应该在浏览器 request
	删除cookie应该在服务器 response
	
3.cookie使用：
	设置cookie：response.set_cookie(key,value）
	获取cookie：username =request.COOKIES.get("username")
	删除cookie：response.delete_cookie("content")
	
	可以加盐：加密 获取的时候需要解密
		加密  response.set_signed_cookie('content', uname, "xxxx")
		解密  
			 获取的是加盐之后的数据
			 	uname = request.COOKIES.get('content)
			 获取的是解密之后数据
			    uname = request.get_signed_cookie("content", salt="xxxx")
		
	通过Response将cookie写到浏览器上，下一次访问，浏览器会根据不同的规则携带cookie过来
		max_age:整数，指定cookie过期时间  单位秒
		expries:整数，指定过期时间，还支持是一个datetime或	timedelta，可以指定一个具体日期时间
		max_age和expries两个选一个指定
		过期时间的几个关键时间
			max_age 设置为 0 浏览器关闭失效
			设置为None永不过期
			expires=timedelta(days=10) 10天后过期
```

```python
def tologinCookie(request):
    return render(request,'loginCookie.html')

def welcomeCookie(request):
    name = request.COOKIES.get('name','客官')
    return render(request,'welcomeCookie.html',context=locals())

def loginCookie(request):
    name = request.POST.get('name')
    response = redirect(reverse('cook:welcomeCookie'))
    response.set_cookie('name',name)
    return response

def logoutCookie(request):
    response = redirect(reverse('cook:welcomeCookie'))
    response.delete_cookie('name')

    return response

# 执行一个视图函数 给name=zs 进行加盐  然后重定向到一个请求  解除加盐
def testSaltCookie(request):
    response = redirect(reverse('cook:testSaltCookie1'))
    response.set_signed_cookie('name','zs',salt='xxx')   
    return response
def testSaltCookie1(request):

    name = request.get_signed_cookie('name',salt='xxx')
    print(name)

    return HttpResponse(name)
```

### 2、session

```tex
1.含义：
服务端会话技术，数据都存储在服务端，默认存在内存 RAM，在django被持久化到了数据库中，该表叫做
Django_session,这个表中有三个字段，分别为seesion_key,session_data,expris_date.
Django中Session的默认过期时间是14天，支持过期，主键是字符串，默认做了数据安全，使用了BASE64
    - 使用的base64之后 那么这个字符串会在最后面添加一个=
    - 在前部添加了一个混淆串
	依赖于cookies
	
2.session使用：
	设置session
		    request.session["username"] = username
	获取session
		    username = request.session.get("username")
	使用session退出
            del request.session['username']
                cookie是脏数据
            response.delete_cookie('sessionid')
                session是脏数据
            request.session.flush()
			冲刷
	session常用操作
		get(key,default=None) 根据键获取会话的值
		clear() 清楚所有会话
		flush() 删除当前的会话数据并删除会话的cookie
		delete request['session_id'] 删除会话
		session.session_key获取session的key
		request.session[‘user’] = username
			数据存储到数据库中会进行编码使用的是Base64
```

```python
def tologinSession(request):
    return render(request,'loginSession.html')


def loginSession(request):
    name = request.POST.get('name')

    request.session['name'] = name

    return redirect(reverse('sess:welcomeSession'))


def welcomeSession(request):
    name = request.session.get('name')
    return render(request,'welcomeSession.html',context=locals())


def logoutSession(request):
    response = redirect(reverse('sess:welcomeSession'))
    # 删除session但是cookie还在
    # del request.session['name']

    # 删除cookie 但是session还在
    # response.delete_cookie('sessionid')

    # session 和 cookie 全部删除
    request.session.flush()

    return response
```

### 3、token

```tex
基本概念：Token 的中文意思是“令牌”。主要用来身份验证。 Facebook，Twitter，Google+，Github 等大型网站都在使用。比起传统的身份验证方法，Token 有扩展性强，安全性高的特点，非常适合用在 Web 应用或者移动应用上,如果使用在移动端或客户端开发中，通常以Json形式传输，服务端会话技术,自定义的Session,给他一个不能重复的字符串,数据存储在服务器中
```

```tex
验证方法：使用基于 Token的身份验证方法，在服务端不需要存储用户的登录记录。大概的流程是这样的：
1.客户端使用用户名跟密码请求登录
2.服务端收到请求，去验证用户名与密码
3.验证成功后，服务端会签发一个 Token，再把这个Token 发送给客户端
4.客户端收到 Token以后可以把它存储起来，比如放在 Cookie里或者 Local Storage里
5.客户端每次向服务端请求资源的时候需要带着服务端签发的Token
6.服务端收到请求，然后去验证客户端请求里面带着的 Token，如果验证成功，就向客户端返回请求的数据
```

```python
python常用Token生成方法：
1.binascii.b2a_base64(os.urandom(24))[:-1]
使用举例：
    >>> import binascii
    >>> import os
    >>> binascii.b2a_base64(os.urandom(24))[:-1]

    b'J1pJPotQJb6Ld+yBKDq8bqcJ71wXw+Xd'
总结：这种算法的优点是性能快， 缺点是有特殊字符， 需要加replace 来做处理。
2.sha1(os.urandom(24)).hexdigest()
使用举例：
    >>> import hashlib
    >>> import os
    >>> hashlib.sha1(os.urandom(24)).hexdigest()

    '21b7253943332d0237a720701bcb8161b82db776'
总结：这种算法的优点是安全，不需要做特殊处理。缺点是覆盖范围差一些。
3.uuid4().hex
使用举例：
    >>> import os
    >>> import uuid
    >>> uuid.uuid4().hex

    'c58a80d3b7864b0686757b95e9626e47'
总结：Uuid使用起来比较方便， 缺点为安全性略差一些。
4.base64.b32encode(os.urandom(20))/base64.b64encode(os.urandom(24))
使用举例：
    >>> import base64
    >>> import os
    >>>base64.b32encode(os.urandom(20))
    b'NJMTBMOYIXHNRATTOTVONT4BXJAC25TX'
    >>>base64.b64encode(os.urandom(24))
    b'l1eU6UzSlWsowm8M8lH5VaFhZEAQ4kQj'

总结：
(1)可以用base64的地方，选择binascii.b2a_base64是不错的选择;
(2)根据W3的SessionID的字串中对identifier的定义，SessionID中使用的是base64，但在Cookie的值内使用需要注意“=”这个特殊字符的存在；
(3)如果要安全字符（字母数字），SHA1也是一个不错的选择，性能也不错；
```

```python
# ================token的应用================
import hashlib

# 待加密内容
strdata = "xiaojingjiaaseafe16516506ng"

h1 = hashlib.md5()
h1.update(strdata.encode(encoding='utf-8'))

strdata_tomd5 = h1.hexdigest()

print("原始内容：", strdata, ",加密后：", strdata_tomd5)

import time
import base64
import hmac


# 生产token
def generate_token(key, expire=3600):
    r'''''
        @Args:
            key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
            expire: int(最大有效时间，单位为s)
        @Return:
            state: str
    '''
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


# 验证token
def certify_token(key, token):
    r'''''
        @Args:
            key: str
            token: str
        @Returns:
            boolean
    '''
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False
        # token certification success
    return True


key = "xiaojingjing"
print("key：", key)
user_token = generate_token(key=key)

print("加密后：", user_token)
user_de = certify_token(key=key, token=user_token)
print("验证结果：", user_de)

key = "xiaoqingqing"
user_de = certify_token(key=key, token=user_token)
print("验证结果：", user_de)
```

### 4、cookie与session的区别

```tex
1、cookie数据存放在客户端上，session数据放在服务器上。
2、cookie不是很安全，别人可以分析存放在本地的COOKIE并进行COOKIE欺骗 
考虑到安全应当使用session。
3、session会在一定时间内保存在服务器上。当访问增多，会比较占用你服务器的性能 
考虑到减轻服务器性能方面，应当使用COOKIE
```

### 5、session与token的区别

```tex
1.作为身份认证 token安全性比session好，因为每个请求都有签名还能防止监听以及重放攻击
2.Session 是一种HTTP存储机制，目的是为无状态的HTTP提供的持久机制。Session 认证只是简单的把User 信息存储到Session 里，因为SID 的不可预测性，暂且认为是安全的。这是一种认证手段。 但是如果有了某个User的SID,就相当于拥有该User的全部权利.SID不应该共享给其他网站或第三方.
3.Token,如果指的是OAuth Token 或类似的机制的话，提供的是 认证 和 授权 ，认证是针对用户，授权是针对App。其目的是让 某App有权利访问 某用户 的信息。这里的 Token是唯一的。不可以转移到其它 App上，也不可以转到其它 用户上。
```

## 四、csrf豁免

```tex
防跨站攻击

实现机制:
1 页面中存在 {% csrf_token %} 时
2 在渲染的时候，会向Response中添加 csrftoken的Cookie
3 在提交的时候，会被添加到请求体中， 会被验证有效性
实例：csrf（https://www.jianshu.com/p/d1407591e8de）

解决csrf的问题/csrf豁免：
1 注释中间件
2 在表单中添加{%csrf_token%}
3 在方法上添加 @csrf_exempt
```

