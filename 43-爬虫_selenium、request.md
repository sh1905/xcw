```tex
1.urllib
    模拟浏览器发送请求 urllib.request.urlopen()
    response的类型以及6个方法
    下载 urllib.request.urlretrieve(url,filename)
    请求对象的定制 urllib.request.Request()
    get
    post
    ajax-get
    ajax-post
    异常
    cookie登陆 人人网 微博
    handler
    代理
    动态cookie
爬取网页中所有的html

2.解析
    正则
    xpath
    jsonpath
    bs4
解析出你想要的源码中的部分数据

3.selenium
    驱动真实的浏览器向服务器发送请求，有很多的网站会检测是否是真实的浏览器
    如果你不是真实的浏览器  那么就会给你做js加密  返回的不是html页面
    而是js数据  那么我们做解析的时候 就不可能获取到真实的数据
    所以要解析js数据

    解析js数据的方案：
                （1）分析js源码  难度大  速度快  花费时间久
                （2）selenium   简单    速度慢  花费时间短
                （3）splush     简单    速度始终 花费时间短

    selenium
            有界面 加载速度慢
                selenium
            无界面 加载速度快
                phantomjs
                handless

4.requests 和 urllib一样的功能

5.scrapy
```

## 一、selenium

```tex
1.什么是selenium?
    (1)Selenium是一个用于Web应用程序测试的工具。
    (2)Selenium测试直接运行在浏览器中，就像真正的用户在操作一样。
    (3)支持各种driver（FirfoxDriver,IternetExploreDriver,OperaDriver,ChromeDriver）驱动真实浏览器完成测试。
    (4)selenium也是支持无界面浏览器操作的。
```

```tex
2.为什么使用selenium？
	模拟浏览器功能，自动执行网页中的js代码，实现动态加载
```

```tex
3.如何安装selenium？
    (1)操作谷歌浏览器驱动下载地址					http://chromedriver.storage.googleapis.com/index.html 
    (2)谷歌驱动和谷歌浏览器版本之间的映射表
    http://blog.csdn.net/huilan_same/article/details/51896672
    (3)查看谷歌浏览器版本
        谷歌浏览器右上角-->帮助-->关于
    (4)pip install selenium
```

```tex
4.selenium的使用步骤？
    (1)导入：from selenium import webdriver
    (2)创建谷歌浏览器操作对象：
        path = '浏览器驱动路径'
        browser = webdriver.Chrom(path)
    (3)访问网址
        url = '要访问的网址'
        browser.get(url)
```

```tex
4-1:selenium的元素定位？
	元素定位：自动化要做的就是模拟鼠标和键盘来操作这些元素，点击输入等等。操作这些元素前首先要找到他们，webDriver提供很多定为的方法：
方法：
    1.find_element_by_id
        eg:button = browser.find_element_by_id('su')
    2.find_elements_by_name
        eg:name = browser.find_element_by_name('wd')
    3.find_elements_by_xpath
        eg:xpath1 =browser.find_elements_by_xpath('//input[@id="su"]')
    4.find_elements_by_tag_name
        eg:names = browser.find_elements_by_tag_name('input')
    5.find_elements_by_css_selector
        eg:my_input = browser.find_elements_by_css_selector('#kw')[0]
    6.find_elements_by_link_text
        eg:browser.find_element_by_link_text("新闻")
```

```python
# selenium-元素定位
from selenium import webdriver

path = 'chromedriver.exe'
browser = webdriver.Chrome(path)

url = 'http://www.baidu.com'
browser.get(url=url)

# id
kw = browser.find_element_by_id('kw')
print(kw)
# name
name = browser.find_elements_by_name('wd')
print(name)
# xpath
xname = browser.find_elements_by_xpath('//input[@id="kw"]')
print(xname)
# bs4
bname = browser.find_elements_by_css_selector('#kw')
print(bname)
# tag_name
tname = browser.find_elements_by_tag_name('input')
print(tname)
# link
lname = browser.find_elements_by_link_text('地图')
print(lname)
browser.quit()
```

```tex
4-2:访问元素信息
获取元素属性
	.get_attribute('value')
获取元素文本
	.text
获取id
	.id
获取标签名
	.tag_name
```

```python
# selenium-元素属性
from selenium import webdriver
path = 'chromedriver.exe'
browser = webdriver.Chrome(path)

url = 'http://www.baidu.com'
browser.get(url=url)

su = browser.find_element_by_id('su')
v = su.get_attribute('value')
print(v)

print(su.text)
print(su.id)  # id的位置 不是id的属性
print(su.tag_name)
```

```tex
4-3:交互
	点击:click()
	输入:send_keys()
	后退操作:browser.back()
	前进操作:browser.forword()
	模拟js滚动条:
		js = 'document.body.scrollTop=100000'
		------------------------------------- 
		js='document.documentElement.scrollTop=100000'
		browser.execute_script(js) 执行js代码
	获取网页源代码:browser.page_source
	退出:browser.quit()
```

```python
# selenium-交互
import time

from selenium import webdriver
path = 'chromedriver.exe'
browser = webdriver.Chrome(path)

url = 'https://book.douban.com/tag/%E6%8E%A8%E7%90%86'
browser.get(url=url)
time.sleep(2)
# 滑动到底部
js = 'document.documentElement.scrollTop=100000'
browser.execute_script(js)
# 下一页
next_page = browser.find_elements_by_css_selector('.next')[0]
next_page.click()
# 再滑到底部（另一种方式）
js = 'document.body.scrollTop=100000'
browser.execute_script(js)
print(browser.page_source)# 打印页面资源
time.sleep(3)
browser.quit()
```



## 二、Phantomjs

```tex
1.什么是Phantomjs?
	(1)是一个无界面的浏览器
	(2)支持页面元素查找，js的执行等
	(3)由于不进行css和gui渲染，运行效率要比正实的浏览器要快很多
```

```tex
2.如何使用Phantomjs?
	(1)获取phantomjs.exe文件的路径
	(2)browser = webdriver.PhantomJS(path)
	(3)browser.get(url)
	扩展：保存屏幕快照
	browser.save_screenshot('baidu.png')
```

```python
from selenium import webdriver
import time

path = 'phantomjs.exe'
browser = webdriver.PhantomJS(path)

url = 'http://www.baidu.com'

browser.get(url=url)

browser.save_screenshot('baidu.png')
time.sleep(2)

t = browser.find_element_by_id('kw')
t.send_keys('韩红')

browser.save_screenshot('baidu1.png')

b = browser.find_element_by_id('su')
b.click()

browser.save_screenshot('baidu2.png')

js='document.documentElement.scrollTop=100000'
browser.execute_script(js)

browser.save_screenshot('baidu3.png')
```

## 三、Chrome handless

```tex
1.系统要求：
	Chrome
		Unix\Linux 系统需要Chrome >= 59
		Windows 系统需要chrome >= 60
	python3.6
	Selenium==3.4*
	ChromDriver==2.31
```

```python
2.配置：
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    chrome_options.binary_location = path

	browser = webdriver.Chrome(chrome_options=chrome_options)

	browser.get('http://www.baidu.com/')
```

```python
3.配置封装：
from selenium import webdriver
#这个是浏览器自带的  不需要我们再做额外的操作
from selenium.webdriver.chrome.options import Options

def share_browser():
    #初始化
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    #浏览器的安装路径    打开文件位置
    #这个路径是你谷歌浏览器的路径
    path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    chrome_options.binary_location = path

    browser = webdriver.Chrome(chrome_options=chrome_options)
    return  browser
# ---------------------------
# 封装调用：
    from handless import share_browser
    browser = share_browser()
    browser.get('http://www.baidu.com/')
    browser.save_screenshot('handless1.png')
```

## 四、requests

```tex
1.文档：
	官方文档
		http://cn.python-requests.org/zh_CN/latest/
	快速上手
		http://cn.python-requests.org/zh_CN/latest/user/quickstart.html
```

```tex
2.安装
	pip install requests
```

```tex
3.response的属性以及类型
	类型：Models.response
	r.text        获取网站源码(字符串形式)
	r.encoding    访问或定制编码方式
	r.url         获取请求的url
	r.content     以二进制形式读取
	r.status_code 相应的状态码
	r.headers     响应的头信息
```

```python
import requests

url = 'http://www.baidu.com'

response = requests.get(url=url)

# print(type(response))
# 以二进制格式来读取文件
# print(response.content)
# 以字符串格式来读取文件
# print(response.text)
# 获取服务器响应的状态码
# print(response.status_code)
print(response.url)
print(response.headers)
# 响应的时候设置编码  打印response.text的时候  那么有乱码发生 那么我们
# 可以使用response.encoding来设置编码
response.encoding = 'utf-8'
```

```python
4.get请求
requests.get()
eg:
    import requests
    url = 'http://www.baidu.com/s?'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    data = {
        'wd':'北京'
    }
    response = requests.get(url,params=data,headers=headers)
content = response.text
print(content)
# ------------------------- 
定制参数:
    参数使用params传递
    参数无需urlencode
    不需要请求对象的定制
    请求资源路径中？可加可不加
```

```python
5.post请求
requests.post()
# 百度翻译
import requests
post_url = 'http://fanyi.baidu.com/sug'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
data = {
    'kw':'eye'
}
response = requests.post(url=post_url,headers=headers,data=data)
content = response.text
import json
obj = json.loads(content)
s = json.dumps(obj,ensure_ascii=False)
print(s)
```

```tex
6.get和post区别？
(1)get请求的参数名字是params;  post请求的参数的名字是data
(2)请求资源路径后面可以不加?
(3)不需要手动编解码
(4)不需要做对象的定制
```

```python
7.proxy定制
在请求中设置proxies参数,参数类型是一个字典类型
eg:
    import requests
    url = 'http://www.baidu.com/s?'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, 			  like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    data = {
        'wd':'ip'
    }
    proxy = {
        'http':'219.149.59.250:9797'
    }
    response = requests.get(url=url,params=data,headers=headers,proxies=proxy)
    content = response.text
    with open('proxy.html','w',encoding='utf-8') as fp:
        fp.write(content)
```

```tex
8.session定制
应用案例：
    （1）笑话集
    http://www.jokeji.cn/
    账号密码	action   action123
    （2）全书网登陆
    账号密码    action    action
    （3）古诗文网（需要验证）
    （4）云打码平台
    用户登陆   actionuser  action
    开发者登陆  actioncode  action
```

```python
# 笑话集-session.get()
import requests

url_get = 'http://www.jokeji.cn/user/c.asp'

data = {
    'u': 'action',
    'p': 'action123',
    'sn': '1',
    't': 'big',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
}

session = requests.session()
# 当通过session去访问的时候 那么会将响应的所有的数据绑定再session上
session.get(url=url_get,params=data,headers=headers)

url = 'http://www.jokeji.cn/User/MemberCenter.asp'
# 再次通过session去访问 那么将会将之前返回的信息提交给该请求
response = session.get(url=url,headers=headers)
# requests默认的编码格式是iso-8859-1
response.encoding = 'gb2312'
content = response.text

with open('xh.html','w',encoding='gb2312')as fp:
    fp.write(content)
```

```python
# 全书网-session.post()
import requests

url = 'http://www.quanshuwang.com/login.php?do=submit'

data = {
    'username': 'action',
    'password': 'action',
    'action': 'login',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
}

session = requests.session()

session.post(url=url,data=data,headers=headers)

url_get = 'http://www.quanshuwang.com/modules/article/bookcase.php'

response = session.get(url=url_get,headers=headers)
response.encoding = 'gbk'
content = response.text
with open('qs.html','w',encoding='gbk')as fp:
    fp.write(content)
```

```python
# 古诗文网
import requests
from bs4 import BeautifulSoup
import urllib.request

url = 'https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
}

session = requests.session()

response = requests.get(url=url,headers=headers)
# 登陆页面的源码
content = response.text

soup = BeautifulSoup(content,'lxml')

viewstate = soup.select('#__VIEWSTATE')[0].attrs.get('value')
viewstategenerator = soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')

code = soup.select('#imgCode')[0].attrs.get('src')
code_url = 'https://so.gushiwen.org' + code


# 有坑。。。
# urllib.request.urlretrieve(url=code_url,filename='code.jpg')
response_code = session.get(url=code_url)
content_code=response_code.content
with open('code.jpg','wb')as fp:
    fp.write(content_code)

codename = input('请输入验证码')
# 提交表单
url_post = 'https://so.gushiwen.org/user/login.aspx?from=http%3a%2f%2fso.gushiwen.org%2fuser%2fcollect.aspx'
data_post = {
    '__VIEWSTATE': viewstate,
    '__VIEWSTATEGENERATOR': viewstategenerator,
    'from': 'http://so.gushiwen.org/user/collect.aspx',
    'email': '595165358@qq.com',
    'pwd': 'action',
    'code': codename,
    'denglu': '登录',
}
response_post = session.post(url=url,headers=headers,data=data_post)
content_post = response_post.text
with open('gushiwen.html','w',encoding='utf-8')as fp:
    fp.write(content_post)
```

