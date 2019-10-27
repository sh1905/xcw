## 一、互联网爬虫介绍

```tex
1.通过一个程序，根据url进行爬取网页，获取有用的信息
2.使用程序模拟浏览器，去向服务器发送请求
```

## 二、爬虫核心

```tex
1.爬取网页：爬取整个网页 包含了网页中所有的内容
2.解析数据：将网页中你得到的数据 进行解析
3.难点：爬虫和反爬虫之间的博弈
```

## 三、爬虫的用途

* 数据分析/人工数据集
* 社交软件冷启动
* 舆情监控
* 竞争对手监控

## 四、爬虫语言分类

```tex
1.php:多进程和多线程支持不好
2.java:目前java爬虫需求岗位旺盛，python爬虫的主要对手，代码臃肿，代码量大、重构成本高，而爬虫需要经常修改，所以不好用
3.C\C++:学习成本比较高，性能和效率高，停留在研究层面，市场需求量小。体现程序员能力。
4.python:语法简洁优美、对新手友好，学习成本低、支持的模块非常多、有scrapy非常强大的爬虫框架
```

## 五、爬虫分类

* 通用爬虫

```tex
实例：
	百度、360、google、sougou等搜索引擎 ---》伯乐在线
功能：
	访问网页->抓取数据->数据存储->数据处理->提供检索服务
robots协议：
	一个约定俗成的协议，添加robots.txt文件，来说明本网站哪些内容不可以被抓取，起不到限制作用
	自己写的爬虫无需遵守
网站排名(SEO)
    1.根据pagerank算法进行排名(参考个网站排名、点击率等指标)
    2.百度竞价排名，钱多就是爸爸
缺点：
	1.抓取到的数据大多是无用的
	2.不能根据用户的需求来精准获取数据

```

* 聚焦爬虫

```tex
功能
	根据需求，实现爬虫程序，抓取需要的数据
原理
    1.网页都有自己唯一的url(统一资源定位符）
    2.网页都是html组成
    3.传输协议都是http\https
设计思路
	1.确定要爬取的url
		如何获取Url
	2.模拟浏览器通过http协议访问url，获取服务器返回的html代码
		如何访问
	3.解析html字符串（根据一定规则提取需要的数据）
		如何解析
```

## 六、爬虫手段

```tex
1.User-Agent:
	User-agent中文名为用户代理，简称UA，它是一个特殊的字符串头，使得服务器能够识别客户使用的操作系统及版本、CPU类型、浏览器及版本、浏览器渲染引擎、浏览器语言浏览器插件等。
2.代理IP
	西次代理
	快代理
	什么是高匿名、匿名和透明代理？他们有什么区别？
	1.使用透明代理，对方的服务器可以知道你使用了代理，并且也知道你的真实IP。
	2.使用匿名代理，对方的服务器知道你使用了代理，但是不知道你的真实IP。
	3.使用高匿名代理，对方服务器不知道你使用了代理，更不知道你的真实IP。
3.验证码访问
	扫码平台
		云打码平台
		超级鹰
4.动态加载网页 网站返回的是js数据 并不是网页的真实数据
	selenium驱动真实的浏览器发送请求
5.数据加密
	分析js代码

爬虫-反爬虫-反反爬虫
```

## 七、HTTP协议

```tex
1.http和https区别？
http
	明文传输，端口号80 无状态
	HTTP协议（HyperText Transfer Protocol，超文本传输协议）：是一种发布和接收HTML的方法，基于TCP/IP通信协议来传递数据。
-------------------
https
	加密传输，端口号443
	HTTPS（Hypertext Transfer Protocol over Secure Socket Layer）简单讲就是HTTP的安全版，在HTTP下加入SSL层。
	HTTPS = HTTP + SSL
--------------------
SSL(Secure Sockets Layer 安全套接层)
	主要用于web的安全协议，在传输层对网络连接进行加密，保障Internet上数据传输的安全。
2.什么是SSL？
SSL
    什么是安全认证
    关于CA
    12306网站证书是自己的
    安全认证requests
    安全认证urllib
注意：如果报错SSL,那么解决方案是
    import urllib.request
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
3.常见服务器端口号
    ftp 		21
    ssh			22
    mysql       3306
    oracle      1521
    MongoDB     27017
    redis       6379
http工作原理
	url（统一资源定位符）组成：
		协议://主机地址:端口号/请求资源路径/?参数1&参数2/#锚点
	上网原理：
		http请求和响应：
            请求行：请求头、请求体
            响应行：响应头、响应体
----------------------------------
请求头详解
Accept           指定客户端能够接收的内容类型
Accept-Encoding  指定浏览器可以支持的web服务器返回内容压缩编码类型。
Accept-Language  浏览器可接受的语言
Cache-Control	 指定请求和响应遵循的缓存机制
Connection		 表示是否需要持久连接。（HTTP 1.1默认进行持久连接）
CookieHTTP		 请求发送时，会把保存在该请求域名下的所有cookie值一起发送给web服务器。
Host     		 请求地址
Upgrade-Insecure-Requests    http是否升级为https
User-Agent 
X-Requested-With             是否是ajax请求             
Referer                      上一级路径
----------------------------------
响应头详解
Connection
Content-Encoding
Content-Type
Date			 生成消息的具体时间和日期
Expires
Set-Cookie		是非常重要的header, 用于把cookie 发送到客户端浏览器,每一个写入cookie都会生成一个Set-Cookie.
ServerWeb		服务器软件名称
Transfer-Encoding            内容是否分包传输
常见HTTP状态码
200 请求成功
404 未找到资源
500 服务器内部错误
```

## 八、urllib库使用

```tex
urllib.request.urlopen()模拟浏览器向服务器发送请求
response  服务器返回的数据
response的数据类型是HttpResponse
	字节 --> 字符串
		解码decode
	字符串 --> 字节
		编码encode
----------------------------
	read()   以字节形式读取二进制 
		     扩展：rede(5)返回前几个字节
	readline()  读取一行
	readlines() 一行一行读取  直至结束
	getcode()   获取状态码
	geturl()	获取url
	getheaders()    获取headers
----------------------------
urllib.request.urlretrieve()
	请求网页
	请求图片
	请求视频
```

## 扩展：编码的由来

```tex
编码集的演变---
由于计算机是美国人发明的，因此，最早只有127个字符被编码到计算机里，也就是大小写英文字母、数字和一些符号，
这个编码表被称为ASCII编码，比如大写字母A的编码是65，小写字母z的编码是122，0的编码是48。
但是要处理中文显然一个字节是不够的，至少需要两个字节，而且还不能和ASCII编码冲突，
所以，中国制定了GB2312编码，用来把中文编进去。
你可以想得到的是，全世界有上百种语言，日本把日文编到Shift_JIS里，韩国把韩文编到Euc-kr里，
各国有各国的标准，就会不可避免地出现冲突，结果就是，在多语言混合的文本中，显示出来会有乱码。
因此，Unicode应运而生。Unicode把所有语言都统一到一套编码里，这样就不会再有乱码问题了。
Unicode标准也在不断发展，但最常用的是用两个字节表示一个字符（如果要用到非常偏僻的字符，就需要4个字节）。
现代操作系统和大多数编程语言都直接支持Unicode。
```

## 九、请求对象的定制

```tex	
UA介绍：User Agent中文名为用户代理，简称UA，它是一个特殊的字符串头，使得服务器能够识别客户使用的操作系统及版本、CPU 类型、浏览器及版本。浏览器内核、浏览器渲染引擎、浏览器语言、浏览器插件等
---------------------------------
语法：request = urllib.request.Request()
```

## 十、编解码

### 1.get请求方式：urllib.parse.quote()

```python
# 单个参数
import urllib.request
import urllib.parse

url = 'https://www.baidu.com/s?wd='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

url = url + urllib.parse.quote('小野')

request = urllib.request.Request(url=url,headers=headers)

response = urllib.request.urlopen(request)

print(response.read().decode('utf-8'))
```

### 2.get请求方式：urllib.parse.urlencode()

```python
# 多个参数
import urllib.request
import urllib.parse
url = 'http://www.baidu.com/s?'
data = {
    'name':'韩美娟',
    'sex':'不知道',
}
data = urllib.parse.urlencode(data)
url = url + data
print(url)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}
request = urllib.request.Request(url=url,headers=headers)
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))
```

### 3.post请求方式

```python
# 百度翻译
import urllib.request
import urllib.parse
url = 'https://fanyi.baidu.com/sug'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}
keyword = input('请输入您要查询的单词')
data = {
    'kw':keyword
}
data = urllib.parse.urlencode(data).encode('utf-8')
request = urllib.request.Request(url=url,headers=headers,data=data)
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))
```

### 总结：post和get区别？

```tex
1.get请求方式必须编码，参数拼接到url后面，编码之后不需要调用encode方法
2.post请求方式的参数必须编码，参数是放在请求对象定制的方法中，编码之后需要调用encode方法
```

### 案例练习：百度详细翻译

```python
import urllib.request
import urllib.parse

url = 'https://fanyi.baidu.com/v2transapi'
headers = {
    # ':authority': 'fanyi.baidu.com',
    # ':method': 'POST',
    # ':path': '/v2transapi',
    # ':scheme': 'https',
    # 'accept': '*/*',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'zh-CN,zh;q=0.9',
    # 'content-length': '119',
    # 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; PSTM=1537097513; BIDUPSID=D96F9A49A8630C54630DD60CE082A55C; BAIDUID=0814C35D13AE23F5EAFA8E0B24D9B436:FG=1; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; H_PS_PSSID=1424_21115_29522_29519_29099_29568_28835_29220_26350; PSINO=2; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1563000604,1563334706,1565592510; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1565592510; yjs_js_security_passport=2379b52646498f3b5d216e6b21c6f1c7bf00f062_1565592544_js',
    # 'origin': 'https://fanyi.baidu.com',
    # 'referer': 'https://fanyi.baidu.com/translate?aldtype=16047&query=&keyfrom=baidu&smartresult=dict&lang=auto2zh',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-origin',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    # 'x-requested-with': 'XMLHttpRequest',
}
data = {
    'from': 'en',
    'to': 'zh',
    'query': 'you',
    'transtype': 'realtime',
    'simple_means_flag': '3',
    'sign': '269482.65435',
    'token': '2e0f1cb44414248f3a2b49fbad28bbd5',
}
#参数的编码
data = urllib.parse.urlencode(data).encode('utf-8')
# 请求对象的定制
request=urllib.request.Request(url=url,headers=headers,data=data)
response = urllib.request.urlopen(request)
# 请求之后返回的所有的数据
content = response.read().decode('utf-8')
import json
# loads将字符串转换为python对象
obj = json.loads(content)
# python对象转换为json字符串  ensure_ascii=False  忽略字符集编码
s = json.dumps(obj,ensure_ascii=False)
print(s)
```

## 十一、ajax的get请求

### 案例：豆瓣电影

```python
# 爬取动画排行榜第一页的前20数据
import urllib.request
import urllib.parse

url = 'https://movie.douban.com/j/chart/top_list?type=25&interval_id=100%3A90&action=&start=0&limit=20'

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
}

request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
context = response.read().decode('utf-8')

with open('douban.json', 'w', encoding='utf-8') as fp:
    fp.write(context)
```

```python
# 请求对象的定制
# 获取服务器响应数据
# 下载
import urllib.request
import urllib.parse

def create_request(page):
    url = 'https://movie.douban.com/j/chart/top_list?type=25&interval_id=100%3A90&action=&'
    data = {
        'start': (page - 1) * 20,
        'limit': 20
    }
    data = urllib.parse.urlencode(data)
    url = url + data
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    }
    request = urllib.request.Request(url=url, headers=headers)
    return request


def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content


def down_load(content):
    with open('douban_'+str(page)+'.json','w',encoding='utf-8') as fp:
        fp.write(content)


if __name__ == '__main__':
    start_page = int(input('请输入起始页码：'))
    end_page = int(input('请输入结束页码：'))
    for page in range(start_page,end_page+1):
        request = create_request(page)
        content = get_content(request)
        down_load(content)
```

## 十二、ajax的post请求

```python
#ajax_post获取kfc店铺地址前20页
import urllib.request
import urllib.parse
import socket
import time

timeout = 20


def create_request(page):
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
    data = {
        'cname': '上海',
        'pid': '',
        'pageIndex': page,
        'pageSize': 10,
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    }

    socket.setdefaulttimeout(timeout)
    # 这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
    sleep_download_time = 10
    time.sleep(sleep_download_time)
    request = urllib.request.Request(url=url, headers=headers, data=data)
    return request


def get_context(request):
    response = urllib.request.urlopen(request)
    context = response.read().decode('utf-8')
    response.close()
    return context


def down_load(page, context):

    with open('kfc_' + str(page) + '.json', 'w', encoding='utf-8') as fp:
        fp.write(context)


if __name__ == '__main__':
    start_page = int(input('请输入起始页码：'))
    end_page = int(input('请输入结束页码：'))
    for page in range(start_page, end_page + 1):
        request = create_request(page)
        context = get_context(request)
        down_load(page, context)

```

## 十三、复杂的get请求-百度贴吧

```python
# 复杂get百度贴吧
import urllib.request
import urllib.parse


def create_request(page):
    url = 'http://tieba.baidu.com/f?kw=python&ie=utf-8&'
    data = {
        'pn': (page-1)*100,
    }
    data = urllib.parse.urlencode(data)
    url = url + data
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    }
    request = urllib.request.Request(url=url, headers=headers)
    return request


def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content


def down_load(page, content):
    with open('tieba_' + str(page) + '.html', 'w', encoding='utf-8') as fp:
        fp.write(content)


if __name__ == '__main__':
    start_page = int(input('请输入起始页码：'))
    end_page = int(input('请输入结束页码：'))
    for page in range(start_page, end_page + 1):
        request = create_request(page)
        content = get_content(request)
        down_load(page, content)
```

