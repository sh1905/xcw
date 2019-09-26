## 一、NoSQL概述

> 如今,大多数的计算机系统(包括服务器、PC、移动设备等)都会产生庞大的数据量。其实,早在
> 2012年的时候,全世界每天产生的数据量就达到了2.5EB(艾字节,
> )。这些数据有很大一部分是由关系型数据库来存储和管理的。实践证明,关系型数据库是实现数据持久化最为重要的方式,它也是大多数应用在选择持久化方案时的首选技术。

> NoSQL 是一项全新的数据库革命性运动,虽然它的历史可以追溯到1998年,但是NoSQL真正深人心
> 并得到广泛的应用是在进入大数据时候以后,业界普遍认为NoSQL是更适合大数据存储的技术方案,这
> 才使得NoSQL的发展达到了了前所未有的高度。2012年年《纽约时报》的一篇专栏中写到,大数据时代已
> 经降临,在商业、经济及其他领域中,决策将不再基于经验和直觉而而是基于数据和分析而作出。事实上,在天文学、气象学、基因组学、生物学、社会学、互联网搜索引擎、金融、医疗、社交网络、电子商务等诸多领域,由于数据过于密集和庞大,在数据的分析和处理上也遇到了了前所未有的限制和阻碍,
> 这一切都使得对大数据处理技术的研究被提升到了新的高度,也使得各种NoSQL的技术方案进入到了公众的视野。

NoSQL数据库按照其存储类型可以大致分为以下几类:

| 类型       |                                      |      |
| ---------- | ------------------------------------ | ---- |
| 列族数据库 | HBase<br />Cassandra<br />Hypertable | 顾名思义是按列存储数据的。最大的特点是方方便存储结构化和半结构化数据,方便做数据压缩,对针对某一列或者某几列的查询有非常大的I/O优势,适合于批量数据处理和即时查询 |
| 文档数据库 | MongoDB<br />CouchDB<br />ElasticSearch | 文档数据库一般用类JSON格式存储数据,存储的内容是文档型的。这样也就有机会对某些字段建立索引,实现关系数据库的某些功能,但不提供对参照完整性和分布事务的支持。 |
| K-V数据库  | DynamoDb<br />Redis<br />LevelDB | 可以通过key快速查询到其value，有基于内存和基于磁盘两种方式。 |
| 图数据库   | Ne04J<br />FlockDB<br />JanusGraph | 使用图结构进行语义查询的数据库，它使用节点、边和属性来表示和存储数据。图数据库从设计上，就可以简单快速的检索难以在关系系统中建模的复杂层次结构。 |
| 对象数据库 | db4o<br />Versant | 通过类似面向对象语言的语法操作数据库，通过对象的方式存储数据。 |



## 二、Redis 入门

Redis 是一种基于键值对的NoSQL数据库,它提供了对多种数据类型(字符串、哈希、列表、集合、有序集合、位图等)的支持,能够满足很多应用场景的需求。

Redis将数据放在内存中,因此读写性能是非常惊人的。与此同时,Redis也提供了持久化机制,能够将内存中的数据保存到硬盘上,在发生意外状况时数据也不不会丢掉。此外,Redis还支持键过期、地理信息运算、发布订阅、事务、管道、Lua脚本
扩展等功能,总而言之,Redis的功能和性能都非常强大,如果项目中要实现高速缓存和消息队列这样
的服务,直接交给Redis就可以了。

目前,国内外很多著名的企业和商业项目都使用了Redis,包括:
Twitter、Github、StackOverflow、新浪微博、百度、优酷土豆、美团、小米、唯品会等。

### 1.Redis简介

2008年,一个名为Salvatore Sanfilippo的程序员为他开发的LOG项目定制了专属的数据库(因为之前他无论怎样优化MySQL,系统性能已经无法再提升了),这项工作的成果就是Redis的初始版本。
后来他将Redis的代码放到了了全球最大的代码托管平台Github,从那以后,Redis引发了大量开发者的好
评和关注,继而有数百人参与了Redis的开发和维护,这使得Redis的功能越来越强大和性能越来越好。
Redis是 remote dictionary server 的缩写,它是一个用 ANSI C 编写的高性能的key-value存储系统,
与其他的key-value存储系统相比,Redis有以下一些特点(也是优点):

* Redis的读写性能极高,并且有丰富的特性(发布/订阅、事务、通知等)。

* Redis支持数据的持久化(RDB和AOF两种方式),可以将内存中的数据保存在磁盘中,重启的时
  候可以再次加载进行使用。

* Redis支持多种数据类型,包括:string、hash、list、set,zset、bitmap、hyperloglog等。

* Redis支持主从复制(实现读写分析)以及哨兵模式(监控master是否宕机并自动调整配置)。

* Redis支持分布式集群,可以很容易的通过水平扩展来提升系统的整体性能。
* Redis基于TCP提供的可靠传输服务进行通信,很多编程语言都提供了Redis客户端支持。

### 2.Redis的应用场景

* 高速缓存 - 将不常变化但又经常被访问的热点数据放到Redis数据库中,可以大降低关系型数据库的压力,从而提升系统的响应性能。
  
* 排行榜 - 很多网站都有排行榜功能,利用Redis中的列表和有序集合可以非常方便的构造各种排行榜系统。
  
* 商品秒杀/投票点赞 - Redis提供了对计数操作的支持,网站上常见的秒杀、点赞等功能都可以利用
  Redis的计数器通过+1或-1的操作来实现,从而避免了使用关系型数据的update 操作。

* 分布式锁 - 利用Redis可以跨多台服务器实现分布式锁(类似于线程锁,但是能够被多台机器上的
  多个线程或进程共享)的功能,用于实现一个阻塞式操作。

* 消息队列 - 消息队列和高速缓存一样,是一个大型网站不可缺少的基础服务,可以实现业务解耦和
  非实时业务削峰等特性。

### 3.Redis的安装和配置

可以使用 Linux 系统的包管理工具 apt 来安装 Redis: `apt install redis` 

也可以通过在Redis的 官方网站 下载 Redis 的源代码,解压缩解归档之后通过 make工具对源代码进行构建并安装。

```bash
wget http://download.redis.io/releases/redis-5.0.5.tar.gz
tar -xzf redis-5.0.5.tar
cd redis-5.0.5
make && make install
```

### 4.Redis的配置

在redis源代码目录下有一个名为redis.conf的配置的文件：

1. 配置将Redis服务绑定到指定的IP地址和端口。

   ```shell
   bind 127.0.0.1
   port 6379
   ```

2. 设置后台运行（以守护进程方式运行）

   ```shell
   daemonize yes
   ```

3. 设置日志级别，可选值：(`debug`：调试，`verbose`：详细，`notice`：通知，`waring`：警告)

   ```shell
   loglevel warning
   ```

4. 配置数据库的数量，默认为16个

   ```shell
   databases 16
   ```

5. 配置数据写入规则

   ```shell
   save 900 1 # 900 秒 (15 分钟) 内修改过 1 个 key, , 写入一次数据库
   
   save 300 10 # 300 秒 (5 分钟) 内修改过 10 个 key, 写入一次数据库
   
   save 60 10000 # 60 秒 (1 分钟) 内修改过 10000 个 key, 写入一次数据库
   ```

   

6. 配置Redis的持久化机制 - RDB。

   ```shell
   rdbcompression yes  # 压缩 RDB 文文件
   rdbchecksum yes     # 对 RDB 文件进行校验
   dbfilename dump.rdb # RDB 数据库文件的文件名
   dir ./              # RDB 文件保存的目录
   ```

7. 配置Redis的持久化机制 - AOF。

   ```shell
   appendonly no
   appendfilename "appendonly.aof"
   ```

8. 配置Redis的主从复制,通过主从复制可以实现读写分离。

   ```shell
   # Master-Replica replication. Use replicaof to make a Redis instance a copy of
   # another Redis server. A few things to understand ASAP about Redis
   replication.
   #
   # +------------------+ 		+---------------+
   # |      Master	     | ---> |    Replica    |
   # | (receive writes) |      |  (exact copy) |
   # +------------------+      +---------------+
   #
   
   # 1) Redis replication is asynchronous, but you can 
   # configure a master to stop accepting writes if it appears # to be not connected with at least a given number of 
   # replicas.
   # 2) Redis replicas are able to perform a partial 
   # resynchronization with the master if the replication link # is lost for a relatively small amount of time. You may 
   # want to configure the replication backlog size (see the 
   # next sections of this file) with a sensible value 
   # depending on your needs.
   # 3) Replication is automatic and does not need user
   # intervention. After a network partition replicas 
   # automatically try to reconnect to masters and 
   # resynchronize with them.
   ```

   

9. 配置慢查询。

   ```shell
   slowlog-log-slower-than 10000 
   # 一次操作超过 10000 毫秒被视作一次慢查询
   slowlog-max-len 128 # 最多纪录 128 次满查询
   ```

### 5.Redis服务器和客户端

* 启动Redis服务器：以下使用指定的配置文件启动Redis服务器

```shell
redis-server 
```

* 用Redis客户端去连接服务器。

```shell
redis-cli 
```

Redis有着非常丰富的数据类型,也有很多的命令来操作这些数据,具体的内容可以查看Redis命令参考,在这个`http://redisdoc.com/`网站,除了Redis的命令参考,还有Redis的详细文档,其中包括了通知、事务、主从复制、持久化、哨兵、集群等内容。

![1568361975208](./images/1568361975208.png)

```shell
# 字符串
127.0.0.1:6379> set username admin
OK
127.0.0.1:6379> get username
"admin"
127.0.0.1:6379> set password "123456" ex 300 #设置过期时间，以秒计
OK
127.0.0.1:6379> get password
"123456"
127.0.0.1:6379> ttl username # 返回给定key的剩余时间
(integer) -1
127.0.0.1:6379> ttl password
(integer) 286
# 哈希
127.0.0.1:6379> hset stu1 name hao
(integer) 0
127.0.0.1:6379> hset stu1 age 38
(integer) 1
127.0.0.1:6379> hset stu1 gender male
(integer) 1
127.0.0.1:6379> hgetall stu1 #返回所有stu1中所有的元素和值
1) "name"
2) "hao"
3) "age"
4) "38"
5) "gender"
6) "male"
127.0.0.1:6379> hkeys stu1 #返回哈希表所有的域
1) "name"
2) "age"
3) "gender"
127.0.0.1:6379> hvals stu1 #返回哈希表stu1中所有域的值
1) "hao"
2) "38"
3) "male"
# hset&hget一次只能往哈希结构里面插入一个键值对，如果插入多个可以用hmset&hmget
127.0.0.1:6379> hmset stu2 name wang age 18 gender female tel 13566778899 # 同时将多个field-value(域-值)对设置到哈希表中
OK
127.0.0.1:6379> hgetall stu2 #返回哈希表stu2中所有的域和值
1) "name"
2) "wang"
3) "age"
4) "18"
5) "gender"
6) "female"
7) "tel"
8) "13566778899"
# 列表
127.0.0.1:6379> lpush nums 1 2 3 4 5
(integer) 5
127.0.0.1:6379> lrange nums 0 -1 #返回列表中指定区间内的元素，区间以偏移量 start 和 stop 指定。
1) "5"
2) "4"
3) "3"
4) "2"
5) "1"
127.0.0.1:6379> lpop nums
"5"
127.0.0.1:6379> lpop nums
"4"
127.0.0.1:6379> rpop nums
"1"
127.0.0.1:6379> rpop nums
"2"
# 集合
127.0.0.1:6379> sadd fruits apple banana orange apple grape 
(integer) 4
127.0.0.1:6379> scard fruits #返回集合中元素的数量
(integer) 4
127.0.0.1:6379> smembers fruits #返回集合中所有成员
1) "grape"
2) "orange"
3) "banana"
4) "apple"
127.0.0.1:6379> sismember fruits apple #判断元素是否是集合成员
(integer) 1
127.0.0.1:6379> sismember fruits durian
(integer) 0
127.0.0.1:6379> sadd nums1 1 2 3 4 5
(integer) 5
127.0.0.1:6379> sadd nums2 2 4 6 8
(integer) 4
127.0.0.1:6379> sinter nums1 nums2 #交集
1) "2"
2) "4"
127.0.0.1:6379> sunion nums1 nums2 #并集
1) "1"
2) "2"
3) "3"
4) "4"
5) "5"
6) "6"
7) "8"
127.0.0.1:6379> sdiff nums1 nums2 #差集
1) "1"
2) "3"
3) "5"
127.0.0.1:6379> zadd topsinger 5234 zhangxy 1978 chenyx 2235 zhoujl 3520 xuezq
(integer) 4
127.0.0.1:6379> zrange topsinger 0 -1 #返回有序集合中，指定区间内的成员。
1) "chenyx"
2) "1978"
3) "zhoujl"
4) "2235"
5) "xuezq"
6) "3520"
7) "zhangxy"
8) "5234"
127.0.0.1:6379> zrevrange topsinger 0 -1
1) "zhangxy"
2) "xuezq"
3) "zhoujl"
4) "chenyx"
# 地理位置geo
127.0.0.1:6379> geoadd pois 116.39738549206541 39.90862689286386 tiananmen
116.27172936413572 39.99
135172904494 yiheyuan 117.27766503308104 40.65332064313784 gubeishuizhen
(integer) 3
127.0.0.1:6379> geodist pois tiananmen gubeishuizhen km
"111.5333"
127.0.0.1:6379> geodist pois tiananmen yiheyuan km
"14.1230"
127.0.0.1:6379> georadius pois 116.86499108288572 40.40149669363615 50 km
withdist
1) 1) "gubeishuizhen"
   2) "44.7408"
```

### 6.在Python程序中使用Redis

使用pip安装Redis模块：`pip install redis`。

redis模块的核心是名为Redis的类,该类的对象代表一个Redis客户端,通过该客户端可以向Redis服务器发送命令并获取执行的结果。

```shell
>>> import redis
>>> client = redis.Redis()
>>> client.set('username', 'admin')
True
>>> client.hset('student', 'name', 'hao')
1
>>> client.hset('student', 'age', 38)
1
>>> client.keys('*')
[b'username', b'student']
>>> client.get('username')
b'admin'
>>> client.hgetall('student')
{b'name': b'hao', b'age': b'38'}
```

redis命令不区分大小写，所以get var和GET var是等价的

| Redis keys命令       | 描述                                                         |
| -------------------- | ------------------------------------------------------------ |
| del  key             | 该命令用于在 key 存在是删除 key。                            |
| dump  key            | 序列化给定 key ，并返回被序列化的值。                        |
| exists  key          | 检查给定 key 是否存在。                                      |
| expire key seconds   | 为给定 key 设置过期时间。                                    |
| keys  pattern        | 查找所有符合给定模式( pattern)的 key 。例如keys * 返回所有的key |
| move  key db         | 将当前数据库的 key 移动到给定的数据库 db 当中。              |
| persist  key         | 移除 key 的过期时间，key 将持久保持。                        |
| PTTL key             | 以毫秒为单位返回 key 的剩余的过期时间。                      |
| TTL key              | 以秒为单位，返回给定 key 的剩余生存时间(TTL, time to live)。 |
| random  key          | 从当前数据库中随机返回一个 key 。                            |
| rename key newkey    | 修改 key 的名称                                              |
| renamenx  key newkey | 仅当 newkey 不存在时，将 key 改名为 newkey 。                |
| type  key            | 返回 key 所储存的值的类型。                                  |



## 三、MongoDB概述

### 1.MongoDB简介

MongoDB 是一个基于分布式文件存储的数据库。

> MongoDB是2009年问世的一个面向文档的数据库管理系统，由 C++ 语言编写,旨在为Web应用提供可扩展的高性能数据存储解决方案。虽然在划分类别的时候后，MongoDB被认为是NoSQL的产品，但是它更像一个介于关系数据库和非关系数据库之间的产品，在非关系数据库中它功能最丰富，最像关系数据库。

> MongoDB将数据存储为一个**文档**，一个文档由一系列的“键值对”组成,其文档**类似于JSON对象**，但是
> MongoDB对JSON进行了**二进制处理**(能够更快的定位key和value)，因此其文档的存储格式称为
> **BSON**。关于JSON和BSON的差别，可以看看MongoDB官方方网站的文章《JSON and BSON》。

> 目前，MongoDB已经提供了对Windows、MacOS、Linux、Solaris等多个平台的支持，而且也提供了多种开发语言的驱动程序，Python当然是其中之一。

### 2.MongoDB的安装和配置

* Linux系统安装和配置MongoDB：`apt install mongodb`

```shell
> wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-3.6.5.tgz
> gunzip mongodb-linux-x86_64-amazon-3.6.5.tgz
> mkdir mongodb-3.6.5
> tar -xvf mongodb-linux-x86_64-amazon-3.6.5.tar --strip-components 1 -C mongodb-3.6.5/
> export PATH=$PATH:~/mongodb-3.6.5/bin
> mkdir -p /data/db
mongod --bind_ip 172.18.61.250
2018-06-03T18:03:28.232+0800 I CONTROL
[initandlisten] MongoDB starting :
pid=1163 port=27017 dbpath=/data/db 64-bit host=iZwz97tbgo9lkabnat2lo8Z
2018-06-03T18:03:28.232+0800 I CONTROL [initandlisten] db version v3.6.5
2018-06-03T18:03:28.232+0800 I CONTROL [initandlisten] git version:
a20ecd3e3a174162052ff99913bc2ca9a839d618
2018-06-03T18:03:28.232+0800 I CONTROL
OpenSSL 1.0.0-fips29 Mar 2010
...
[initandlisten] OpenSSL version:2018-06-03T18:03:28.945+0800 I NETWORK
[initandlisten] waiting for
connections on port 27017
```

> 说明:上面的操作中，export命令是设置PATH环境变量，这样可以在任意路径下执行mongod来
> 启动MongoDB服务器。
>
> MongoDB默认保存数据的路径是`/data/db`目录，为此要提前创建该目
> 录。此外，在使用mongod启动MongoDB服务器时，`--bind_ip`参数用来将服务绑定到指定的IP地址，也可以用`--port`参数来指定端口，默认端口为**27017**。

### 3.MongoDB基本概念

通过与关系型数据库进行对比的方式来说明MongoDB的概念。

| SQL         | MongoDB    | 解释(SQL/MongoDB)    |
| ----------- | ---------- | -------------------- |
| database    | database   | 数据库/数据库        |
| table       | collection | 二维表/集合          |
| row         | document   | 记录(行)/文档        |
| columan     | field      | 字段(列)/域          |
| index       | index      | 索引/索引            |
| table joins |            | 表连接/嵌套文档      |
| primary key | primary    | 主键/主键(`_id`字段) |

### 4.通过shell操作MongoDB

启动服务器后可以使用交互式环境跟服务器通信，如下所示：

```bash
mongo --host 127.0.0.1
MongoDB shell version v3.6.5
connection to: mongodb://127.0.0.1:27017/
```

1. 查看、创建和删除数据库。

   ```bash
   > // 显示所有数据库
   > show dbs
   admin 0.000GB
   config 0.000GB
   local 0.000GB
   > use school// 创建并切换到school数据库
   switched to db school
   > db.dropDatabase()// 删除当前数据库
   { "ok" : 1 }
   > MongoDB 中默认的数据库为 test，如果你没有创建新的数据库，集合将存放在 test 数据库中。
   ```
   
2. 创建、删除和查看集合。
   ```bash
   > use school// 创建并切换到school数据库
   switched to db school
   > db.createCollection('colleges')// 创建colleges集合
   { "ok" : 1 }
   > db.createCollection('students')// 创建students集合
   { "ok" : 1 }
   > show collections// 查看所有集合 show tables
   colleges
   students
   > db.colleges.drop()// 删除colleges集合
   true
   ```
   > 说明：在MongoDB中插入文档是如果集合不存在会自动创建，所以也可以按照下面的方式通      过创建文档来创建集合。
3. 文档的CURD操作。
   ```bash
   > // 向students集合插入文档
   > db.students.insert({stuid: 1001, name: '骆昊', age: 38})
   WriteResult({ "nInserted" : 1 })
   > // 向students集合插入文档
   > db.students.save({stuid: 1002, name: '王大大锤', tel: '13012345678',
   gender: '男'})
   WriteResult({ "nInserted" : 1 })
   > // 查看所有文档
   > db.students.find()
   { "_id" : ObjectId("5d7b6846021c46a91af7d4f7"), "stuid" : 1001,  
   "name" : "zhangsan", "age" : 28 }
   { "_id" : ObjectId("5d7b68a0021c46a91af7d4f8"), "stuid" : 1002, 
   "name" : "lisi", "tel" : "1386666666", "gender" : "male" }
   > // 更新stuid为1001的文档
   > db.students.update({stuid: 1001}, {'$set': {tel: '13566778899', gender:
   'male'}})
   WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
   > // 插入或更新stuid为1003的文文档
   > db.students.update({stuid: 1003}, {'$set': {name: 'wangwu', tel:'13022223333', gender: 'male'}},upsert=true)
   > // 查询所有文档
   > db.students.find().pretty()
   {
   	"_id" : ObjectId("5d7b6846021c46a91af7d4f7"),
   	"stuid" : 1001,
   	"name" : "zhangsan",
   	"age" : 28,
   	"gender" : "male",
   	"tel" : "13299999999"
   }
   {
   	"_id" : ObjectId("5d7b68a0021c46a91af7d4f8"),
   	"stuid" : 1002,
   	"name" : "lisi",
   	"tel" : "1386666666",
   	"gender" : "male"
   }
   {
   	"_id" : ObjectId("5d7b9a1e6c3a650679c9c39b"),
   	"stuid" : 1003,
   	"gender" : "male",
   	"name" : "wangwu",
   	"tel" : "13022223333"
   }
   > // 查询stuid大大于1001的文文档只显示name和tel字段
   > db.students.find({stuid: {'$gt': 1001}}, {_id: 0, name: 1, tel:1}).pretty()
   { "name" : "lisi", "tel" : "1386666666" }
   { "name" : "wangwu", "tel" : "13022223333" }
   
   > // 查询name为“zhangsan”或者tel为“1386666666”的文文档
   > db.students.find({'$or': [{name: 'zhangsan'}, {tel: '1386666666'}]}, {_id:0, name: 1, tel: 1}).pretty()
   { "name" : "zhangsan", "tel" : "13299999999" }
   { "name" : "lisi", "tel" : "1386666666" }
   
   > // 查询学生文档跳过第1条文档只查1条文文档
   > db.students.find().skip(1).limit(1).pretty()
   {
   	"_id" : ObjectId("5d7b68a0021c46a91af7d4f8"),
   	"stuid" : 1002,
   	"name" : "lisi",
   	"tel" : "1386666666",
   	"gender" : "male"
   }
   
   > // 对查询结果进行排序(1表示升序,-1表示降序)
   > db.students.find({}, {_id: 0, stuid: 1, name: 1}).sort({stuid: -1})
   { "stuid" : 1003, "name" : "wangwu" }
   { "stuid" : 1002, "name" : "lisi" }
   { "stuid" : 1001, "name" : "zhangsan" }
   
   > // 在指定的一个或多个字段上创建索引
   > db.students.ensureIndex({name: 1})
   {
   	"createdCollectionAutomatically" : false,
   	"numIndexesBefore" : 2,
   	"numIndexesAfter" : 2,
   	"note" : "all indexes already exist",
   	"ok" : 1
   }
   >
   ```

> 使用MongoDB可以非常方便的配置数据复制，通过冗余数据来实现数据的高可用以及灾难恢复，也可以通过数据分片来应对数据量迅速增长的需求。关于MongoDB更多的操作可以查阅官方文档 ,同时推荐阅读Kristina Chodorow写的《MongoDB权威指南》。

### MongoDB 与 RDBMS Where 语句比较

如果你熟悉常规的 SQL 数据，通过下表可以更好的理解 MongoDB 的条件语句查询：

| 操作       | 格式                     | 范例                                        | RDBMS中的类似语句       |
| :--------- | :----------------------- | :------------------------------------------ | :---------------------- |
| 等于       | `{<key>:<value>`}        | `db.col.find({"by":"菜鸟教程"}).pretty()`   | `where by = '菜鸟教程'` |
| 小于       | `{<key>:{$lt:<value>}}`  | `db.col.find({"likes":{$lt:50}}).pretty()`  | `where likes < 50`      |
| 小于或等于 | `{<key>:{$lte:<value>}}` | `db.col.find({"likes":{$lte:50}}).pretty()` | `where likes <= 50`     |
| 大于       | `{<key>:{$gt:<value>}}`  | `db.col.find({"likes":{$gt:50}}).pretty()`  | `where likes > 50`      |
| 大于或等于 | `{<key>:{$gte:<value>}}` | `db.col.find({"likes":{$gte:50}}).pretty()` | `where likes >= 50`     |
| 不等于     | `{<key>:{$ne:<value>}}`  | `db.col.find({"likes":{$ne:50}}).pretty()`  | `where likes != 50`     |

### 5.在Python程序中操作MongoDB

可以通过`pip install pymongo`来实现对MongoDB的操作。

```bash
>>> import pymongo
>>> cli=pymongo.MongoClient()
>>> cli.sh1905.student.insert({'zhd':100,'hxp':79,'zy':88,'qjg':100clicli.sh1905.student.find()sh1905.student.insert_one({'aaa':12345,'bbb':67890}) 
>>> for i in cli.sh1905.student.find(): 
	print(i)
>>> cli.sh1905.student.count_documents({'aaa':12345})
```

```bash
>>> from pymongo import MongoClient
>>> client = MongoClient('mongodb://120.77.222.217:27017')
>>> db = client.school
>>> for student in db.students.find():
... print('学号:', student['stuid'])
... print('姓名:', student['name'])
... print('电话:', student['tel'])
...
学号: 1001.0
姓名: zhangsan
电话: 13299999999
学号: 1002.0
姓名: lisi
电话: 1386666666
学号: 1003.0
姓名: wangwu
电话: 13022223333
>>>db.students.db.students.count_documents({'tel':1386666666}) 
1
>>> db.students.remove()
{'n': 3, 'ok': 1.0}
```

插入集合 `insert_one()` 方法返回 **InsertOneResult** 对象，该对象包含 **inserted_id** 属性，它是插入文档的 **id** 值。

集合中插入多个文档使用 **insert_many()** 方法，该方法的第一参数是字典列表。也可以指定**_id**来插入。

**find_one()** 方法来查询集合中的一条数据。

**find()** 方法可以查询集合中的所有数据，类似 SQL 中的 **SELECT \*** 操作。可以使用 find() 方法来查询指定字段的数据，将要返回的字段对应值设置为 1。

```bash
for x in mycol.find({},{ "_id": 0, "name": 1, "alexa": 1 }):
  print(x)
```

在 MongoDB 中使用 **update_one()** 方法修改文档中的记录。该方法第一个参数为查询的条件，第二个参数为要修改的字段。如果要修改所有匹配到的记录，可以使用 **update_many()**。

**sort()** 方法可以指定升序或降序排序。第一个参数为要排序的字段，第二个字段指定排序规则，**1** 为升序，**-1** 为降序，默认为升序。

可以使用 **delete_one()** 方法来删除一个文档，该方法第一个参数为查询对象，指定要删除哪些数据。

可以使用 **delete_many()** 方法来删除多个文档，该方法第一个参数为查询对象，指定要删除哪些数据;**delete_many()** 方法如果传入的是一个空的查询对象，则会删除集合中的所有文档：使用 **drop()** 方法来删除一个集合。

