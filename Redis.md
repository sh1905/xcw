## Redis简介

> REmote DIctionary Server(Redis) 是一个由Salvatore Sanfilippo写的key-value存储系统。
>
>  Redis是一个开源的使用ANSI C语言编写、遵守BSD协议、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API。 
>
>  它通常被称为数据结构服务器，因为值（value）可以是 字符串(String), 哈希(Hash), 列表(list), 集合(sets) 和 有序集合(sorted sets)等类型。

### 特点：

* 支持数据的持久化，可以将内存中的数据保存到磁盘中，重启的时候可以再次加载进行使用。
* 不仅仅支持简单的key-value类型的数据，同时还提供list、set、zset、hash等数据结构的存储。
* 支持数据的备份，即master-slave模式的数据备份。

### Redis 优势：

- 性能极高 – Redis能读的速度是110000次/s,写的速度是81000次/s 。
- 丰富的数据类型 – Redis支持二进制案例的 Strings, Lists, Hashes, Sets 及 Ordered Sets 数据类型操作。
- 原子 – Redis的所有操作都是原子性的，意思就是要么成功执行要么失败完全不执行。单个操作是原子性的。多个操作也支持事务，即原子性，通过MULTI和EXEC指令包起来。
- 丰富的特性 – Redis还支持 publish/subscribe, 通知, key 过期等等特性。

```sql
1.安装Redis：`sudo apt install redis-server`

2.启动Redis：`redis-server`

3.查看Redis是否启动：`redis -cli`，有时候会有中文乱码，要在 redis-cli 后面加上 --raw。

-- 以上命令将打开以下终端：
redis 127.0.0.1:6379> ping
PONG
-- 127.0.0.1 是本机 IP ，6379 是 redis 服务端口。现在我们输入 PING 命令。以上说明我们已经成功安装了redis。
```



## Redis数据类型

### 1、String(字符串)

string是Redis最基本的数据类型，可以理解成与Memcached一样的数据类型，一个key-对应一个value。

string 类型是二进制安全的。意思是 redis 的 string 可以包含任何数据。比如jpg图片或者序列化的对象。

 string 类型是 Redis 最基本的数据类型，string 类型的值最大能存储 512MB。 

实例：

```sql
127.0.0.1:6379> set test "Hello World!"
OK
127.0.0.1:6379> get test
"Hello World!"

-- 在以上实例中我们使用了 Redis 的 SET 和 GET 命令。键为 test，对应的值为 Hello world!。
-- 注意：一个键最大能存储 512MB。
```

### 2、Hash(哈希)

Redis hash 是一个键值(key=>value)对集合。

Redis hash 是一个string类型的 field(字段) 和 value 的映射表，hash 特别适合用于存储对象。

实例：

```sql
-- DEL test 用于删除前面测试用过的 key，不然会报错：(error) WRONGTYPE Operation against a key holding the wrong kind of value

127.0.0.1:6379> del test
(integer) 1
127.0.0.1:6379> hmset test field1 "Hello" field2 "World"
OK
127.0.0.1:6379> hget test field1
"Hello"
127.0.0.1:6379> hget test field2
"World"

-- 实例中用到了Redis hmset,hget命令，hmset设置两个field=>value对，hegt 获取对应field对应的value。
-- 每个 hash 可以存储 232 -1 键值对（40多亿）。
```

### 3、List(列表)

Redis列表是简单的字符串列表，按照插入的顺序排序。你可以添加一个元素到列表的头部（左边）或者尾部（右边）。

实例：

```sql
127.0.0.1:6379> del test
(integer) 1
127.0.0.1:6379> lpush test redis
(integer) 1
127.0.0.1:6379> lpush test mongobd
(integer) 2
127.0.0.1:6379> lpush test rabitmq
(integer) 3
127.0.0.1:6379> lrange test 0 10
1) "rabitmq"
2) "mongobd"
3) "redis"
-- 每个列表可存储40多亿元素
```

### 4、Set（集合）

Redis的**Set是string类型的无序集合**。

集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是O(1)。

* sadd 命令
  * 添加一个 string 元素到 key 对应的 set 集合中，成功返回1，如果元素已经在集合中返回 0，如果 key 对应的 set 不存在则返回错误。
  * 语法：`sadd key member`

实例：

```sql
127.0.0.1:6379> sadd test redis
(integer) 1
127.0.0.1:6379> sadd test mongodb
(integer) 1
127.0.0.1:6379> sadd test mongodb
(integer) 0
127.0.0.1:6379> sadd test rabitmq
(integer) 1
127.0.0.1:6379> smembers test
1) "redis"
2) "rabitmq"
3) "mongodb"
-- 注意：以上实例中 rabitmq 添加了两次，但根据集合内元素的唯一性，第二次插入的元素将被忽略。
```

### 5、zset(sorted set：有序集合)

 Redis  zset 和 set 一样也是string类型元素的集合,且不允许重复的成员。
不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。

zset的成员是唯一的,但分数(score)却可以重复。

* zadd 命令
  * 添加元素到集合，元素在集合中存在则更新对应score
  * 语法：`zadd key score member`

实例：

```sql
27.0.0.1:6379> del test
(integer) 1
127.0.0.1:6379> zadd test 0 redis
(integer) 1
127.0.0.1:6379> zadd test 1 mongodb
(integer) 1
127.0.0.1:6379> zadd test 2 rabitmq
(integer) 1
127.0.0.1:6379> zrangebyscore test 0 1000
1) "redis"
2) "mongodb"
3) "rabitmq"

```

### 各个数据类型应用场景：

| 类型                 | 简介                                                   | 特性                                                         | 场景                                                         |
| :------------------- | :----------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| String(字符串)       | 二进制安全                                             | 可以包含任何数据,比如jpg图片或者序列化的对象,一个键最大能存储512M | ---                                                          |
| Hash(字典)           | 键值对集合,即编程语言中的Map类型                       | 适合存储对象,并且可以像数据库中update一个属性一样只修改某一项属性值(Memcached中需要取出整个字符串反序列化成对象修改完再序列化存回去) | 存储、读取、修改用户属性                                     |
| List(列表)           | 链表(双向链表)                                         | 增删快,提供了操作某一段元素的API                             | 1,最新消息排行等功能(比如朋友圈的时间线) 2,消息队列          |
| Set(集合)            | 哈希表实现,元素不重复                                  | 1、添加、删除,查找的复杂度都是O(1) 2、为集合提供了求交集、并集、差集等操作 | 1、共同好友 2、利用唯一性,统计访问网站的所有独立ip 3、好友推荐时,根据tag求交集,大于某个阈值就可以推荐 |
| Sorted Set(有序集合) | 将Set中的元素增加一个权重参数score,元素按score有序排列 | 数据插入集合时,已经进行天然排序                              | 1、排行榜 2、带权重的消息队列                                |

## Redis命令

Redis 命令用于在 redis 服务上执行操作。要在 redis 服务上执行命令需要一个 redis 客户端。

语法：`$ redis-cli`

**在远程服务上执行命令**

如果需要在远程 redis 服务上执行命令，同样我们使用的也是 **redis-cli** 命令。

- 语法：`$ redis-cli -h host -p port -a password`

- 实例：

  ```sql
  -- 以下实例演示了如何连接到主机为 127.0.0.1，端口为 6379 ，密码为 mypass 的 redis 服务上。
  $redis-cli -h 127.0.0.1 -p 6379 -a "mypass"
  redis 127.0.0.1:6379>
  redis 127.0.0.1:6379> PING
  PONG
  ```



