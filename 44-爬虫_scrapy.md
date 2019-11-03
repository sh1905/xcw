```tex
allowed_domains=[只有域名]    允许访问的域名(多页下载)
start_urls=[注意末尾的/]
settings.py文件的反扒
	ROBOTSTXT_OBEY=False     robots协议
	DEFAULT_REQUEST_HEADERS  请求头
	先在parse方法  print打印测试一下  看能否进入到函数内
xpath语法遇到img标签时，找不到图片 记住懒加载  src2
										 lazy-src
scrapy.Request(url=url,callback='parse函数不加圆括号')
```

## 一、scrapy

```tex
1.scrapy是什么？
	Scrapy是一个为了爬取网站数据，提取结构性数据而编写的应用框架。
可以应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序用。
```

```tex
2.安装scrapy：
	pip install scrapy
安装过程中出错：
  如果安装有错误！！！！
  pip install Scrapy
  building 'twisted.test.raiser' extension
  error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ 			 Build Tools": http://landinghub.visualstudio.com/visual-cpp-build-tools
  解决方案：
		http://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted 
		下载twisted对应版本的whl文件（如我的Twisted-17.5.0-cp36-cp36m-win_amd64.whl），cp后面是            python版本，amd64代表64位，运行命令：
		pip install C:\Users\...\Twisted-17.5.0-cp36-cp36m-win_amd64.whl
		pip install Scrapy
  如果再报错   win32
  解决方法：
  		pip install pypiwin32
  再报错：使用anaconda
```

### 1.scrapy项目的创建以及运行

```tex
1.创建scrapy项目:终端输入
	scrapy startproject 项目名称
```

```tex
2.项目组成：
spiders
	__init__.py   自定义的爬虫文件.py---》由我们自己创建，是实现爬虫核心功能的文件
__init__.py		  
items.py ---》定义数据结构的地方，是一个继承自scrapy.Item的类
middlewares.py ---》 中间件代理
pipelines.py ---》 管道文件，里面只有一个类，用于处理下载数据的后续处理  默认是300优先级越小优先级越高(1-1000)
settings.py	---》配置文件  比如：是否遵守robots协议，User-Agent定义等
```

```tex
3.创建爬虫文件：
(1)跳转到spiders文件夹 
	cd 项目名/项目名/spiders
(2)scrapy genspider 爬虫文件名 网页的域名
-------------------------
爬虫文件的基本组成：
class ZzSpider(scrapy.Spider) ---》继承scrapy.Spider类
name = 'baidu' ---》 运行爬虫文件时使用的名字
allowed_domains ---》 爬虫允许的域名，在爬取的时候，如果不是此域名之下的url，会被过滤掉 注意创建爬虫文件的时候域名一般不加http
start_urls ---》 声明了爬虫的起始地址，可以写多个url，一般是一个
parse(self, response) ---》解析数据的回调函数
	response.text ---》获取网页源码
	response.body ---》相应的是二进制文件
	response.url
	response.status
	response.xpath()-》xpath方法的返回值类型是selector对象
	extract() ---》提取的是selector对象的是data
	extract_first() ---》提取的是selector列表中的第一个数据
```

```python
# 汽车之家
# -*- coding: utf-8 -*-
import scrapy


class ChSpider(scrapy.Spider):
    name = 'ch'
    allowed_domains = ['https://car.autohome.com.cn/price/brand-33.html']
    # scrapy爬虫的时候 页面后面加/一般情况下都是一个无效的页面路径
    start_urls = ['https://car.autohome.com.cn/price/brand-33.html']

    # response是执行了起始的url之后的响应久相当于 requests.get的response
    # 获取是urllib。request.urlopen的response
    def parse(self, response):
        print('===================')
        # 获取网页源码
        # print(response.text)
        # 获取的是二进制文件
        # print(response.body)
        # scrapy可以直接的调用xpath方法 而不需要我们获取网页源码之后再进行解析
        # xpath方法返回的数据类型是selector对象
        # 这个对象中有2个参数 第一个参数是xpath 语法  第二参数是data 解析出来的值
        src_list = response.xpath('//div[@class="list-cont-img"]/a/img/@src')
        for src in src_list:
            # 如果获取seletor对象的值呢？
            print(src.extract())
        print('===================')
```

```tex
4.运行爬虫文件
	scrapy crawl  爬虫文件名
	注意：应在spaiders文件夹内执行
扩展：导出文件
    -o name.json
    -o name.xml
    -o name.csv
```

```python
# 58同城
# -*- coding: utf-8 -*-
import scrapy


class CitySpider(scrapy.Spider):
    name = 'city'
    allowed_domains = ['https://sh.58.com/chuzu/?utm_source=markrt']
    start_urls = ['https://sh.58.com/chuzu/?utm_source=markrt/']

    def parse(self, response):
        city_list = []
        li_list = response.xpath('//ul[@class="house-list"]/li[@class="house-cell"]')
        for li in li_list:
            # selector对象可以再次使用xpath语法 但是开头要加 ./ 表示当前目录
            # selector 对象提取数据 那么使用的extract方法
            # selector 列表提取数据 那么使用的extract_first方法
            src = li.xpath('./div[@class="img-list"]/a/img/@lazy_src').extract_first()
            des = li.xpath('./div[@class="des"]/h2/a/text()').extract_first()
            city={}
            city['src']=src
            city['des']=des
            city_list.append(city)
        return city_list
```

### 2.scrapy架构组成

```tex
(1)引擎  ---》自动运行，无需关注，会自动组织所有的请求对象，分发给下载器
(2)下载器  ---》从引擎处获取到请求对象后，请求数据
(3)spiders ---》Spider类定义了如何爬取某个(或某些)网站。包括了爬取的动作(例如：是否更进连接)以及如何从网页的内容中提取到结构化数据(爬取item)。换句话说，Spider就是你定义爬取的动作及分析某个网页(或者有些网页)的地方。
(4)调度器  ---》有自己的调度规则，无需关注
(5)管道(Item pipline) ---》最终处理数据的管道，会预留接口供我们处理数据
-------------------
当Item在Spider中被收集之后，它将会传递到Item Pipeline,一些组件会按照一定的顺序执行对Item的处理。
每个Item Pipeline组件(有时称之为“Item Pipeline”)是实现了简单方法的python类。他们接收到Item的处理，或是被丢弃而不用再进行处理。
以下是item pipeline的一些典型应用：
1.清理HTML数据
2.验证爬取的数据(检查item包含某些字段)
4.将爬取的结果保存到数据库中
```

### 3.scrapy工作原理

![](D:\迅雷下载\第二阶段资料\课件\1029\doc\scrapy原理.png)

![](D:\迅雷下载\第二阶段资料\课件\1029\doc\scrapy原理_英文.png)

## 二、scrapy shell

```tex
1.什么是scrapy shell?
	Scrapy终端，是一个交互终端，供您在未启动spider的情况下尝试及调试您爬取的代码。其本意是用来测试提取数据的代码，不过您可以将其作为正常的Python终端，在上面测试任何的python代码。该终端是用来测xpath
或者css表达式，查看他们的工作方式及爬取的网页中提取的数据。在编写您的spider时，该终端提供了交互性测试您的表达式代码的功能，免去了每次修改后运行spider的麻烦。一旦熟悉了Scrapy终端后，您会发现其开发和调试spider发挥的巨大作用。
```

```tex
2.安装ipython
安装：pip install ipython
简介：如果您安装了 IPython ，Scrapy终端将使用 IPython (替代标准Python终端)。
IPython 终端与其他相比更为强大，提供智能的自动补全，高亮输出，及其他特性。
```

```python
3.应用
(1) scrapy shell  www.baidu.com
(2) scrapy shell  http://www.baidu.com
(3) scrapy shell "http://www.baidu.com"
(4) scrapy shell "www.baidu.com"
语法：
    注意：必须在对应的的项目文件夹下进行操作,
    cd baidu/baidu/spider
（1）response对象：
        response.body
        response.text
        response.url
        response.status
（2）response的解析：
        response.xpath()
            使用xpath路径查询特定元素，返回一个selector列表对象
        response.css()
            使用css_selector查询元素，返回一个selector列表对象
            获取内容 ：response.css('#su::text').extract_first()
            获取属性 ：response.css('#su::attr(“value”)').extract_first()
（3）selector对象（通过xpath方法调用返回的是seletor列表）
        extract()
            使用xpath请求到的对象是一个selector对象，需要进一步使用
            extract()方法拆包，转换为unicode字符串
        extract_first()
            返回第一个解析到的值，如果列表为空，此种方法也不会报错，会返回一个空值
        xpath()
        css()
        注意：每一个selector对象可以再次的去使用xpath或者css方法
（4）item对象
        dict(itemobj)
            可以使用dict方法直接将item对象转换成字典对象
        Item(dicobj)
            可以使用字典对象创建一个Item对象
```

 案例：

1.站长素材 （1）.管道封装（2）.多条管道下载 （3）多页数据下载 

2.电影天堂 （1）一个item包含多级页面的数据 

### 站长素材

```python
# zz.py 
import scrapy
# 注意导包使用 ..上级目录
from ..items import ZhanzhangItem

class ZzSpider(scrapy.Spider):
    name = 'zz'
    allowed_domains = ['sc.chinaz.com']
    start_urls = ['http://sc.chinaz.com/tupian/tiankongtupian.html']
    page = 1
    base_url = 'http://sc.chinaz.com/tupian/tiankongtupian_'

    def parse(self, response):
        img_list = response.xpath('//div[@id="container"]//a/img')
        for img in img_list:
            src = img.xpath('./@src2').extract_first()
            alt = img.xpath('./@alt').extract_first()
            zz = ZhanzhangItem(src=src,alt=alt)
            yield zz
        # 多页数据下载
        if self.page <= 5:
            self.page = self.page+1
            url = self.base_url+str(self.page)+'.html'
            print('========================')
            print(url)
            yield scrapy.Request(url=url,callback=self.parse)
```

```python
# pipelines.py 管道封装+多条管道下载
class ZhanzhangPipeline(object):
    def open_spider(self, spider):
        self.fp = open('zz.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write(str(item))
        return item

    def close_spider(self, spider):
        self.fp.close()
import urllib.request
class ZhanzhangDownLoadPipeline(object):
    def process_item(self, item, spider):
        src = item['src']
        alt = item['alt']
        filename = './mw/'+alt+'.jpg'
        urllib.request.urlretrieve(url=src,filename=filename)
        return item  # 注意return返回值
```

```python
# items.py
import scrapy


class ZhanzhangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    src = scrapy.Field()
    alt = scrapy.Field()
```

### 电影天堂

```python
# mv.py
import scrapy

from ..items import MovieItem


class MvSpider(scrapy.Spider):
    name = 'mv'
    allowed_domains = ['www.ygdy8.net']
    start_urls = ['https://www.ygdy8.net/html/gndy/dyzz/20191030/59293.html']

    def parse(self, response):
        a_list = response.xpath('//div[@id="co_content8"]//b/a')
        for a in a_list:
            name = a.xpath('./text()').extract_first()
            href = a.xpath('./@href').extract_first()
            url = 'https://www.ygdy8.net'+href
            yield scrapy.Request(url=url,callback=self.parse_second,meta={'name':name})   # meta 字典 传递数据
    def parse_second(self,response):
        name = response.meta['name']
        src = response.xpath('//div[@id="Zoom"]//img[1]/@src').extract_first()
        movie = MovieItem(name=name,src=src)
        yield movie
```

```python
# items.py
import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    src = scrapy.Field()
```



## 三、yield

```tex
1.带有yield的函数不再是一个普通函数。而是一个生成器generator，可用于迭代
2.yield是一个类似return的关键字，迭代一次遇到的yield时就返回yield后面(右边)的值。重点是：下一次迭代时，从上一次迭代遇到的yield后面的代码(下一行)开始执行
3.简要理解：yield就是return 每次只返回一个值，并且记住这个返回的位置，下一次迭代就从这个位置后(下一行)开始
```

```python
name_list = [x for x in range(10)] 
def createGenorator():    
    items = []    
    for i in name_list:        
        print('第{}次调用'.format(i))        
        items.append(i)    
        return items 
def testFunc1(): 
    # generator = createGenorator()
	generator = createGenorator2()    
	for a in generator:        
		print('使用第{}次'.format(a))
def createGenorator2():    
    for i in name_list:        
        print('第{}次调用'.format(i))        
        yield i print(testFunc1())
```

## 四、mysql

## 五、pymysql的使用步骤

```tex
1.pip install pymysql
2.conn=pymysql.connetc(host,port,user,password,database,charset)
3.conn.cursor()
4.cursor.execute()
5.conn.commit()
6.conn.close()
```

## 六、CrawlSpider

```tex
1.继承自scrapy.Spider
2.独门秘籍
	CrawlSpider可以定义规则，在解析html内容的时候，可以根据连接规则提取指定的连接，然后再向这些连接发送请求
	所以，如果有需要更进连接的需求，意思是爬取网页之后，需要提取连接再次爬取，使用CrawlSpider是非常合适的
```

```tex
3.提取连接
连接提取器，在这里可以写规则提取指定连接
scrapy.linkextractors.LinkExtractor(
	allow = (),    正则表达式 提取符合正则的连接
	deny = (),     （不用）正则表达式 不提取符合正则的连接
	allow_domains = (),（不用）允许的域名
	deny_domains = (),（不用）不允许的域名
	restrict_xpath = (),xpath 提取符合xpath规则的连接
	restrict_css = (), 提取符合选择器会泽的连接
)
4.模拟使用
	正则用法：links1 = LinkExtractor(allow='list_23\d+\.html')
	xpath用法：links2 = LinkExtractor(restrict_xpaths=r'//div[@class="x"]')        
	css用法：links3 = LinkExtractor(restrict_css='.x') 
5.提取连接        
	link.extract_links(response)
```

```tex
6.注意事项
【注1】callback只能写函数名字符串, callback='parse_item'    
【注2】在基本的spider中，如果重新发送请求，那里的callback写的是   callback=self.parse_item 【注--稍后看】follow=true 是否跟进 就是按照提取连接规则进行提取
```

运行原理：

![](D:\迅雷下载\第二阶段资料\课件\day07\doc\crawlspider运行原理.png)

## 七、CrawlSpider案例

### 需求：读书网数据入库

```tex
1.创建项目：scrapy startproject read
2.跳转到spiders路径 cd read\read\spiders
3.创建爬虫类：scrapy genspider -t crawl readbook www.dushu.com
4.itrms
5.spiders
6.settings
7.pipelines
	数据库保存到本地
	数据库保存到mysql数据库
```

```python
# readbook.py
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ReadItem


class ReadbookSpider(CrawlSpider):
    name = 'readbook'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/book/1107_1.html']

    rules = (
        Rule(LinkExtractor(allow=r'/book/1107_\d+.html'),
                            callback='parse_item',
                            follow=False),
    )

    def parse_item(self, response):
        print('===========')
        img_list = response.xpath('//div[@class="bookslist"]//img')
        for img in img_list:
            src = img.xpath('./@data-original').extract_first()
            name = img.xpath('./@alt').extract_first()
            book = ReadItem(src=src,name=name)
            yield book

```

```python
# items.py
import scrapy


class ReadItem(scrapy.Item):
    name = scrapy.Field()
    src = scrapy.Field()
```

```python
# pipelines
import pymysql


class ReadPipeline(object):
    def open_spider(self, spider):
        self.fp = open('read.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write(str(item))
        return item

    def close_spider(self, spider):
        self.fp.close()


from scrapy.utils.project import get_project_settings


class ReadMysqlPipeline(object):

    def open_spider(self, spider):
        # 建立连接
        self.conn = self.getconn()
        self.cursor = self.conn.cursor()

    def getconn(self):
        settings = get_project_settings()
        conn = pymysql.connect(host=settings['DB_HOST'],
                               user=settings['DB_USER'],
                               password=settings['DB_PASSWORD'],
                               database=settings['DB_DATABASE'],
                               port=settings['DB_PORT'],
                               charset=settings['DB_CHARSET'])
        return conn

    def process_item(self, item, spider):
        sql = 'insert into book1905 values("{}","{}")'.format(item['src'], item['name'])
        self.cursor.execute(sql)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # 关闭连接
        self.cursor.close()
        self.conn.close()
```

```python
# settings.py
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
   # 'read.pipelines.ReadPipeline': 300,
    'read.pipelines.ReadMysqlPipeline':299,
}
DB_HOST='127.0.0.1'
DB_USER='root'
DB_PASSWORD='root'
DB_DATABASE='spider1905'
DB_PORT=3306
DB_CHARSET='utf8'
```

