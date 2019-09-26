## 一、项目拆分

### 1、环境

```tex
开发环境-假数据                   develop
测试环境-数据量大一些   假数据  	   test
演示环境-类似线上环境也叫预生产环境   show
线上环境-也叫做生产环境 真实数据	  product
```

```python
# settings.py
# dialect:drover://username:passwor@host:port/database
def get_database_uri(DATABASE):
    dialect=DATABASE.get('dialect')
    driver = DATABASE.get('driver')
    username = DATABASE.get('username')
    password = DATABASE.get('password')
    host = DATABASE.get('host')
    port = DATABASE.get('port')
    database = DATABASE.get('database')
    return '{}+{}://{}:{}@{}:{}/{}'.format(dialect,driver,username,password,host,port,database)

class Config():
    Test=False
    Debug=False
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class DevelopConfig(Config):
    Debug = True
    DATABASE = {
        'dialect':'mysql',
        'driver':'pymysql',
        'username':'xcw',
        'password':'182562',
        'host':'localhost',
        'port':'3306',
        'database':'day041905',
    }
    SQLALCHEMY_DATABASE_URI=get_database_uri(DATABASE)

class TestConfig(Config):
    Test = True
    DATABASE = {
        'dialect': 'mysql',
        'driver': 'pymysql',
        'username': 'xcw',
        'password': '182562',
        'host': 'localhost',
        'port': '3306',
        'database': 'day041905',
    }
    SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)

class ShowConfig(Config):
    DATABASE = {
        'dialect': 'mysql',
        'driver': 'pymysql',
        'username': 'xcw',
        'password': '182562',
        'host': 'localhost',
        'port': '3306',
        'database': 'day041905',
    }
    SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)


class ProductConfig(Config):
    DATABASE = {
        'dialect': 'mysql',
        'driver': 'pymysql',
        'username': 'xcw',
        'password': '182562',
        'host': 'localhost',
        'port': '3306',
        'database': 'day041905',
    }

    SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)

ENV_NAME={
    'develop':DevelopConfig,
    'test':TestConfig,
    'show':ShowConfig,
    'product':ProductConfig
}
```



### 2、拆分项目

* 规划项目结构

  ```tex
  manager.py
  	app.py的创建
  	交给 Manager 管理（flask-script管理对象）
  	蓝图注册
  App
  	__init__.py
  	  |	 创建Flask对象
  	  |	 加载settings文件
  	  |	 调用init_ext方法
  	  V	 调用init_blue方法
  	settings
        |  App运行的环境配置
        V  SQLALCHEMY_TRACK_MODIFICATIONS运行环境
      ext（扩展的，额外的）
          用来初始化第三方的各种插件
          Sqlalchemy属性配置 
          db.init_app 数据库
          Session初始化(持久化)
      views
          蓝图
          创建
      	注册到manager上
      models
      	定义模型
      	sqlalchemy对象初始化
  ```

```python
# ext.py
from flask_migrate import Migrate
from flask_session import Session

from App.models import db
# from App.settings import DevelopConfig


def init_ext(app):
    # flask-session
    app.config['SECRET_KEY']='110'
    app.config['SESSION_TYPE']='redis'
    app.config['SESSION_KEY_PREFIX']='python1905'
    Session(app=app)


    # 如果参数的传递的是类  那么会将这个类变为一个对象  该对象就具备了 SQLALCHEMY_DATABASE_URI
    # 和 SQLALCHEMY_TRACK_MODIFICATIONS
    app.config.from_object(DevelopConfig)

    # flask-sqlalchemy
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    # app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:1234@localhost:3306/day041905'
    # 注意 init_app方法 一定要在初始化参数的下面
    # 如果报错SQLALCHEMY_TRACK_MODIFICATIONS  那么要么是单词写错 要么是初始化没有在init_app方法之上
    db.init_app(app=app)
    # flask-migrate
    migrate = Migrate()
    migrate.init_app(app=app,db=db)
```



## 二、flask-migrate

使用步骤：模型迁移 （ 模型 -----》 表 ）

### 1、安装

```bash
pip install flask-migrate
```

### 2、初始化

1. 创建migrate对象  **ext**

   ```python
   # 需要将 app 和 db 初始化 ===>ext.py
   migrate = Migrate()
   migrate.init_app(app=app,db=db)
   ```

2. 懒加载初始化  **manager**

   ```python
   # 结合 flask-script 使用
   # 在 manager 上添加 command(MigrateCommand)
   
   manager.add_command('db',MigrateCommand)
   ```

3. 执行`python manager.py db xx`

   ```tex
   1 init      第一次使用
   2 migrate 	生成迁移文件
   		  	不能生成有 2 中情况：
   		  	(1) 模型定义完成从未调用
   		  	(2) 数据库已经有模型记录
   		  	解决方法：删除库中已经存在的所有表
   		  	drop table;
   3 upgrade 	升级，执行迁移文件
   4 downgrade 降级，撤销前面生成的表
   扩展：创建用户文件(给迁移文件添加自己的后缀名)
   python manager.py db -message '创建用户'
   注意：如果之前没有migrations的文件夹 那么必须先init，但是如果有这个文件夹 那么就不需要init了。
   ```



## 三、DML

```tex
DDL  数据定义语言
        针对表操作    create  alter  drop

DML  数据操纵语言
		针对数据的操作 insert delete update

DQL  数据查询语言   select

TCL  事务         commit rollback
```

### 1、增

* 创建对象

  ```python
  1 添加一个对象：db.session.add()
  
  @blue.route('/addStudent/')
  def addStudent():
      s = Student()
      s.name = 'zs'
      s.age = 18
      db.session.add(s)
      db.session.commit()
      return '添加一个成功'
  
  2 添加多个对象：db.session.add_all()
  
  @blue.route('/addStudentList/')
  def addStudentList():
      student_list =[]
      for i in range(5):
          s = Student()
          s.name='小明%d' %i
          s.age = i
          student_list.append(s)
      db.session.add_all(student_list)
      db.session.commit()
      return '添加多个成功'
  ```

### 2、删除

  `db.session.delete(对象)==>基于查询`

```python
@blue.route('/deleteStudent/')
def deleteStudent():
    # 删除一定要建立在查询的基础上
    s=Student.query.first()
    print(s.name,s.age)
    db.session.delete(s)
    db.session.commit()
    return '删除成功'
```

### 3、修改 

 `db.session.add(对象)===>基于查询`

```python
@blue.route('/updateStudent/')
def updateStudent():
    s = Student.query.first()
    s.name = 'ls'
    db.session.add(s)
    db.session.commit()
    return '修改成功'
```

### 4、DML 查

#### 1.获取单个数据  

* 返回的数据类型是一个 模型类

```python
1 get
	主键值：获取不到不会报错
    person = Person.query.get(3)
    db.session.delete(person)
    db.session.commit()
2 first
	person = Person.query.first()
```

```python
@blue.route('/getOne/')
def getOne():
    s = Student.query.first()
    print(type(s))
    print(s.name,s.age)
    # 注意没有last方法
    # s1 = Student.query.last()
    # print(s1.name,s1.age)
    s2 = Student.query.get(2)
    print(type(s2))
    print(s2.name,s2.age)

    return '查询成功'
```

#### 2.获取结果集  

* 返回的是BaseQuery对象

```python
（1）xxx.query.all   
 	persons = Person.query.all()
	返回的列表的类型
（2）xxx.query.filter_by
	persons = Person.query.filter_by(p_age=15)
	返回的是BaseQuery对象
（3）xxx.query.filter
    persons = Person.query.filter(Person.p_age < 18)
    persons = Person.query.filter(Person.p_age.__le__(15))
    persons = Person.query.filter(Person.p_name.startswith("小"))
    persons = Person.query.filter(Person.p_name.endswith("1"))
    persons = Person.query.filter(Person.p_name.contains("1"))
    persons = Person.query.filter(Person.p_age.in_([15, 11]))
    返回的是BaseQuery对象
```

```python
# 获取结果集  
# all     返回的是一个列表
# filter_by  
# filter  关注的就是返回值类型

@blue.route('/getResult/')
def getResult():
    # 查询id为2的数据
    # filter和filter_by
    # 对主键字段的操作(注意：filter不需要加模型类名Student)
    student_list = Student.query.filter_by(id=2)
    print(type(student_list))
    student_list = Student.query.filter(id==2)
    print(type(student_list))
   	# filter和filter_by
	# 对非主键字段的操作(注意：filter需要加模型类名Student)
   	student_list = Student.query.filter_by(age = 2)
  	print(type(student_list))
   	student_list = Student.query.filter(Student.age == 2)
   	print(type(student_list))
   
   	# student_list = Student.query.filter(Student.age.__gt__(2))
   	# student_list = Student.query.filter(Student.age.__lt__(2))
    # student_list = Student.query.filter(Student.age > 2)
    # student_list = Student.query.filter(Student.name.startswith('小'))
    # student_list = Student.query.filter(Student.name.endswith('1'))
    # student_list = Student.query.filter(Student.name.contains('小'))
    # student_list = Student.query.filter(Student.age.__lt__(2))
    student_list = Student.query.filter(Student.age.in_([1,2]))
    for student in student_list:
        print(student.name,student.age)
        print(type(student_list))
        return '查询结果集成功' 
```

```tex
扩展：
(1) user = User.query.get(id=3)
    print(user.name)

    默认情况下在调用get方法的时候就发送了sql语句

    如果我们使用了dynamic 那么就代表的是懒加载或者叫做延迟加载
    在不使用对象的属性或者方法的时候就不发送sql语句

(2) users = User.query.all()
    for user in users:
        print(user.name)

    默认情况下在调用get方法的时候就发送了sql语句
    如果我们使用了dynamic 那么就可以在遍历的时候发送sql语句
```

#### 3.数据筛选

```tex
（1）order_by
    升序：
    persons = Person.query.order_by("p_age")
    降序：
    persons = Person.query.order_by(db.desc('p_age'))
（2）limit
	persons = Person.query.limit(5)
（3）offset
	persons = Person.query.offset(5).order_by("id")
（4）offset和limit不区分顺序，offset先生效
    persons = Person.query.order_by("id").limit(5).offset(5)
    persons = Person.query.order_by("id").limit(5)
    persons = Person.query.order_by("id").offset(17).limit(5)
（5）order_by 需要先调用执行(order_by无论在语法还是执行顺序都是先执行)
	persons = Person.query.order_by("id").offset(17).limit(5)
```



#### 4.pagination分页

```python
（1）简介：分页器
    需要想要的页码
    每一页显示多少数据
（2）原生：
	persons = Person.query.offset((page_num - 1) * page_per).limit(page_per)
（3）封装：
	参数（page，page_per,False(是否抛异常）
    persons = Person.query.paginate(page_num, page_per, False).items
```

```python
# ===============================
# 分页原生代码
#  一页有几条数据  page_per/pagesize    第几页  page
@blue.route('/getPage/')
def getPage():
    page = int(request.args.get('page'))
    page_per = int(request.args.get('page_per'))

    # 1页  2  0   (1-1)*2
    # 2页  2  2   (2-1)*2
    # 3页  2  4   (3-1)*4
    student_list = Student.query.limit(page_per).offset((page-1)*page_per)
    for student in student_list:
        print(student.id,student.name,student.age)
# ================================
# 分页封装
@blue.route('/getPageFz/')
def getPageFz():

    pagination = Song.query.paginate(page=1,per_page=5).items

    for p in pagination:
        print(p.name)

    return '分页成功'
```



#### 5.逻辑运算

```python
（1）与and_     filter(and_(条件))
song = Song.query.filter(and_(Song.id==1,Song.name=='晴天'))[0]

（2）或or_      filter(or_(条件))
song = Song.query.filter(or_(Song.id == 1,Song.name=='香水有毒'))[0]

（3）非not_     filter(not_(条件))  注意条件只能有一个
songs = Song.query.filter(not_(Song.name == '香水有毒'))
for song in songs:
    print(song.id,song.name)
（4）in
songs = Song.query.filter(Song.id.in_([1,2,3,4]))
for song in songs:
    print(song.id,song.name)
```



### 5、数据定义类型

```python
（1）字段类型
    Integer
    String
    Date
    Boolean
（2）约束
    primary_key   （主键）   			
    autoincrement （主键自增长）     			
    unique        （唯一） 			
    default       （默认）   			
    index         （索引）    			
    nullable      （非空）			
    ForeignKey    （外键）                       
        用来约束级联数据
        db.Column( db.Integer, db.ForeignKey=True )
        使用relationship实现级联数据获取
        声明级联数据
        backref="表名"
        lazy=True
```

### 6、模型关系

#### 1.一对多

```python
（1）模型定义
class Parent(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(30),unique=True)
    children=db.relationship("Child",backref="parent",lazy=True)
    

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
```



```python
（2）参数介绍:
1.relationship函数
    sqlalchemy对关系之间提供的一种便利的调用方式，关联不同的表；
2.backref参数
    对关系提供反向引用的声明，在Address类上声明新属性的简单方法，之后可以在my_address.person来获取这个地址的person；
3.lazy参数
    （1）'select'（默认值）
	SQLAlchemy 会在使用一个标准 select 语句时一次性加载数据；
    （2）'joined'
    让 SQLAlchemy 当父级使用 JOIN 语句是，在相同的查询中加载关系；
    （3）'subquery'
    类似 'joined' ，但是 SQLAlchemy 会使用子查询；
    （4）'dynamic'：
    SQLAlchemy 会返回一个查询对象，在加载这些条目时才进行加载数据，大批量数据查询处理时推荐使用。
4.ForeignKey参数
    代表一种关联字段，将两张表进行关联的方式，表示一个person的外键，设定上必须要能在父表中找到对应的id值
```

```python
（3）模型应用
# 一对多
# 添加
@blue.route('/addParent/')
def addParent():
    parent = Parent()
    parent.name = '张三'


    child = Child()
    child.name = '张四'

    child1 = Child()
    child1.name = '王五'

    child_list = [child,child1]

    parent.children = child_list

    db.session.add(parent)
    db.session.commit()

    return '添加成功'


# 查询  应用级
# 主查从    给你一个parent  然后查询child的孩子
@blue.route('/getChild/')
def getChild():
    childs = Child.query.filter(Parent.id == 1)

    for child in childs:
        print(child.name)

    return '查询成功了兄弟'

# 从查主    给一个child  查询parent
@blue.route('/getParent/')
def getParent():

    parent = Parent.query.filter(Child.id == 1)[0]
    print(parent.name)

    return '查询成功了兄弟'




# class Parent(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(30), unique=True)
#
# class Child(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), unique=True)
#     parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))


# 如果不加relationship
# 查询 给主表数据 然后查询从表数据
@blue.route('/getChild1/')
def getChild1():
    parent = Parent.query.filter(Parent.id == 1)[0]
    childs = Child.query.filter(Child.parent_id == parent.id)
    for child in childs:
        print(child.name)

    return '查询成功'



# class Parent(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(30), unique=True)
#     children = db.relationship("Child")
#
# class Child(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), unique=True)
#
#     parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))

# 加relationship
@blue.route('/getChild2/')
def getChild2():
    parent = Parent.query.filter(Parent.id == 1)[0]
    childs = parent.children
    for child in childs:
        print(child.name)

    return '查询成功'


# class Parent(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(30), unique=True)
#
#     children = db.relationship("Child", backref="parent", lazy=True)
#
#
# class Child(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), unique=True)
#
#     parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))

# 加backref
@blue.route('/getParent1/')
def getParent1():
    child = Child.query.filter(Child.id == 1)[0]
    print(child.parent.name)
    return '查询成功'
```



#### 2.一对一

```python
# 一对一需要设置relationship中的uselist=Flase，其他数据库操作一样。
#     一对一  和 一对多所有的使用方式 完全一致
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32))
    # uselist=False 是在模型执行的时候  会验证 从表中是否有重复的数据
    address = db.relationship('Address',backref='user',lazy=True,uselist=False)


class Address(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32))
    user_id = db.Column(db.ForeignKey('user.id'))
```



#### 3.多对多

```python
（1）模型定义
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32))
    age = db.Column(db.Integer,default=18)

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32))

class Collection(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    u_id = db.Column(db.Integer,db.ForeignKey(User.id))
    m_id = db.Column(db.Integer,db.ForeignKey(Movie.id))
```

```python
（2）应用场景
# 多对多
class User1(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32))


class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32))


class Collection(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    u_id = db.Column(db.ForeignKey(User1.id))
    m_id = db.Column(db.ForeignKey(Movie.id))

    num = db.Column(db.Integer,default=1)


class Movie1(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32))
    # 导演
    director = db.Column(db.String(32))
    # 领衔主演
    starring = db.Column(db.String(128))
    # 上映时间
    showtime = db.Column(db.String(128))
    # 简介
    brief = db.Column(db.String(256))
    # 时长
    duration = db.Column(db.String(128))
```

**count方法判断BaseQuery对象是否有数据，因为查询BaseQuery对象不会报错**

```python
# 多对多
# 需求：第一次会插入到数据库   第二次会在原来的基础之后 数量加1


@blue.route('/addCollection/')
def addCollection():
    u_id = int(request.args.get('u_id'))
    m_id = int(request.args.get('m_id'))

    collections = Collection.query.filter(Collection.u_id == u_id).filter(Collection.m_id == m_id)

    # collection.count() 获取basequery的元素长度
    if collections.count() > 0:
        collection = collections[0]
        collection.num = collection.num + 1
        print(1111)
    else:
        collection = Collection()
        collection.u_id = u_id
        collection.m_id = m_id
        print(2222)
    db.session.add(collection)
    db.session.commit()


    return '添加成功'

# ============================
# flask-bootstrap
# <head>
#       head
#             title
#             metas
#             styles

# <body>
#        body
#            navbar
#            content
#            script

@blue.route('/bootstrapDemo/')
def bootstrapDemo():
    page = int(request.args.get('page',1))
    per_page = request.args.get('per_page',5)

    pagination = Movie1.query.paginate(page=page,per_page=per_page)

    return render_template('bootstrapDemo.html',pagination=pagination,page=page)
```





   


