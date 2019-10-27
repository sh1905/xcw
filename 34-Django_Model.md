## 一、修改数据库

```python
1.在settings.py中的DATABASE中进行修改:
'ENGINE':'django.db.backends.mysql',# 引擎
'NAME':数据库名,
'USE':用户名,
'PASSWORD':密码,
'HOST':主机,
'PORT':端口号  # 注意：加不加引号 '' 都可以
```

```python
2.注意迁移时的驱动问题：
(1)mysqlclient:python2/3都能直接使用，致命缺点-对安装有要求，必须制定位置存在配置文件
(2)mysql-python: - python2 支持很好，- python3不支持。
(3)pymysql: 会伪装成mysqlclient和mysql-python;
python2, python3都支持：
注意：在项目目录下init中书写
# -----------------------------
import pymysql
pymysql.install_as_mysqldb()
```

## 二、DML数据库操纵语言

```tex
数据操作
1.迁移
    生成迁移文件
        python manage.py makemigrations
    执行迁移文件
        python manage.py migrate
2.ORM
	Object Relational Mapping 对象关系映射
	将业务逻辑和sql进行了一个解耦合
	通过models定义实现 数据库表的定义
3.模型定义
	(1)继承自models.Model   （flask继承自db.Model）
	(2)会自动增加主键列
	(3)必须指定字符串类型属性的长度
	classs Student(models.Model):
		name = models.CharField(max_length=16)
		age = models.IntegerField(default=18)
	------------------------------------------
	存储数据
		创建对象进行save()
	数据查询
		模型.objects.all()
		模型.objects.get(pk=2) （pk:primary key）
	更新
		基于查询
		save()
	删除
		基于查询
		delete()
```

## 三、Django Shell

```python
使用：Django 终端，命令是：
	python manage.py shell
	集成了django环境的python 终端，通常用来调试。

from Two.models import Student
students = Stuednt.objects.all()
for student in students:
    print(students.name)
```

## 四、数据级联

```python 
一对多模型关系：
	class Grade(models.Model):
      g_name = models.CharField(max_length=32)

    class Student(models.Model):
          s_name =models.CharField(max_length=16)
          s_grade=models.ForeignKey(Grade)
案例：
(1)多获取一方，根据学生找班级名字  
显性属性：就是你可以在类中直接观察到的属性---->通过多方获取一方，那么可以使用使用多方调用显性属性直接获取一方数据。
    student = Student.objects.get(pk=2)
    grade = student.s_grade
    return HttpResouce(grade.g_name)
(2)一方获取多方，根据班级找所有的学生
隐性属性：就是我们在类中观察不到的，但是可以使用的属性--->通过一方获取多方 ，那么可以使用一方属性的隐性属性获取多方数据
    grade = Grade.objects.get(pk=2)
    students = grade.sutdent_set.all()
    content = {
        'students':students
    }
    return render(request,'students_list.html',content)
```

```python
# -------------models.py------------
# 一对多
class Men(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    class Meta:
        db_table='men'
class Women(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    w_men = models.ForeignKey(Men)
    class Meta:
        db_table='women'
# -------------views.py--------------
# 当一对多关系时候  那么可以通过主表的对象.从表模型的小写_set 来获取从表中的所有的对应数据
# eg：men = Men.objects.get(pk=1)
#     men.women_set

# dept emp        dept.emp_set
# grade student    grade.student_set

# 模型小写_set 是属性  不带（）的我们就叫做属性  那么该属性在主表中没有  那么我们称之为隐性属性
def getWomen(request):
    men = Men.objects.get(pk=1)
    print(type(men))
    women_list = men.women_set.all()
    print(men.women_set)
    for women in women_list:
        print(women.id,women.name,women.age)

    return HttpResponse('查询成功')

# 显性查询
def getMen(request):
    women = Women.objects.get(pk=1)
    men = women.w_men
    print(men.id,men.name,men.age)
    return HttpResponse('查询对象')
```



## 五、元信息

```python
class Meta:
    db_table = '表名'
# 作用：指定表名和字段名
# 注意：表的字段一般都是下划线   如：s_name
#      类的属性一般都是驼峰式   如：sName
```

## 六、定义字段

```tex
1 字段类型：
(1)CharField(max_length=字符长度)
	字符串，默认的表单样式是 TextInput
(2)TextField
	大文本字段，一般超过4000使用，默认的表单控件是Textarea
(3)IntegerField  整数
(4)DecimalField(max_digits=None, decimal_places=None)
    ·使用python的Decimal实例表示的十进制浮点数
    ·参数说明
        ·DecimalField.max_digits
        ·位数总数
        ·DecimalField.decimal_places
        ·小数点后的数字位数

(5)FloatField
	用Python的float实例来表示的浮点数

(6)BooleanField
	true/false 字段，此字段的默认表单控制是CheckboxInput

(7)NullBooleanField
	支持null、true、false三种值

(8)DateField([auto_now=False, auto_now_add=False])
    ·使用Python的datetime.date实例表示的日期
    ·参数说明
        ·DateField.auto_now
        ·每次保存对象时，自动设置该字段为当前时间，
        用于"最后一次修改"的时间戳，它总是使用当前日期，默认为false
       
        ·DateField.auto_now_add
        ·当对象第一次被创建时自动设置当前时间，
        用于创建的时间戳，它总是使用当前日期，默认为false
        ·说明
            ·该字段默认对应的表单控件是一个TextInput. 
            在管理员站点添加了一个JavaScript写的日历控件，
            和一个“Today"的快捷按钮，包含了一个额外的invalid_date错误消息键
            ·注意
            ·auto_now_add, auto_now, and default 这些设置是相互排斥的，
            他们之间的任何组合将会发生错误的结果

(9)TimeField
	·使用Python的datetime.time实例表示的时间，参数同DateField

(10)DateTimeField
	·使用Python的datetime.datetime实例表示的日期和时间，参数同DateField

(11)FileField
	·一个上传文件的字段

(12)ImageField
	·继承了FileField的所有属性和方法，但对上传的对象进行校验，确保它是个有效的image
------------------------------------------
2 字段选项
    ·概述
    ·通过字段选项，可以实现对字段的约束
    ·在字段对象时通过关键字参数指定
(1)null
	·如果为True，Django 将空值以NULL 存储到数据库中，默认值是 False
(2)blank
	·如果为True，则该字段允许为空白，默认值是 False
        ·注意
        ·null是数据库范畴的概念，blank是表单验证证范畴的
(3)db_column
	·字段的名称，如果未指定，则使用属性的名称
(4)db_index
	·若值为 True, 则在表中会为此字段创建索引
(5)default
	·默认值
(6)primary_key
	·若为 True, 则该字段会成为模型的主键字段
(7)unique
	·如果为 True, 这个字段在表中必须有唯一值
```

```tex
逻辑删除:
    ·对于重要数据都做逻辑删除，不做物理删除，
    ·实现方法是定义isDelete属性，类型为BooleanField，默认值为False
```

## 七、模型过滤（查询）

```python
Django默认通过模型的objects对象实现模型数据查询。
Django有两种过滤器用于筛选记录：
	filter:返回符合筛选条件的数据集
	exclude	:返回不符合筛选条件的数据集
链式调用：
	多个filter和exclude可以连接在一起查询
	Person.objects.filter().filter().xxxx.exclude().exclude().yyyy
	Person.objects.filter(p_age__gt=50).filter(p_age__lt=80)注意数据类型
	Person.objects.exclude(p_age__gt=50)
	Person.objects.filter(p_age__in=[50,60,61])
```

```python
def testFilter(request):
    # filter  方法的返回值类型 是一个queryset类型
    # person = Person.objects.filter(age=12)[0]
    # print(person.id,person.name,person.age)
    # print(type(person))

    # exclude
    # persons = Person.objects.exclude(age=12)
    # for person in persons:
    #     print(person.id,person.name,person.age)

    # 链式调用  无限嵌套  随便写
    # person = Person.objects.exclude(age=12).filter(age=21)[0]
    # print(person.id,person.name,person.age)

    # 应用
    # gt  great than
    # lt  less  than
    # lte less than  equals
    # gte great than equals
    # persons = Person.objects.filter(age__gt=20)
    # for person in persons:
    #     print(person.id,person.name,person.age)

    # persons = Person.objects.filter(age__in=[12,21])
    # for person in persons:
    #     print(person.id,person.name,person.age)

    return HttpResponse('查询成功')
```



## 八、创建对象的方式（四种）

```tex
（1）创建对象1   常用
	person = Person（）   
	person.name='zs'  
	person.age=18
（2）创建对象2
    直接实例化对象，设置属性
    创建对象，传入属性
    使用:
    	person =  Model.objects.create(name='zs',age=18)
		person.save()
    自己封装类方法创建
    在Manager中封装方法创建
（3）创建对象3
	person = Person(name='zs',age=18)
（4）创建对象4
    注意:__init__已经在父类models.Model中使用，在自定义的模型中无法使用
    在模型类中增加类方法去创建对象
    @classmethod  
    def create(cls,name,age=100):
        return cls(name=name,age=age)
    --------------------------
    person = Person.create('zs')
```

```python
def createObject(request):
    # 创建对象1   常用
    # person = Person()
    # person.name = '滨崎步'
    # person.age = 18
    # person.save()

    # 创建对象2
    # person = Person(name='苍井空',age=18)
    # person.save()

    # 创建对象3
    # person = Person.objects.create(name='花泽香菜',age=18)
    # person.save()

    # 创建对象4
    person = Person.create('高桥凉介')
    person.save()

    return HttpResponse('创建成功哈拉扫')
# -----------------------------------
class Person(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    class Meta:
        db_table = 'person'
    @classmethod
    def create(cls,name,age=19):
        return cls(name=name,age=age)
```



## 九、查询集

- 查询集：表示从数据库获取的对象集合，查询集可以有多个过滤器。
- 过滤器：过滤器就是一个函数，基于所给的参数限制查询集结果，返回查询集的方法称为过滤器。

### 查询集：

```tex
查询经过过滤器筛选后返回新的查询集，所以可以写成链式调用。
获取查询结果集  QuerySet
1 all
	模型.objects.all()
2 filter
	模型.objects.filter()
3 exclude
    模型.objects.exclude()
4 order_by
    persons= Person.objects.order_by('id')
    默认是根据id排序
    注意要写的是模型的属性
        
5 values
    persons= Person.objects.order_by('id') persons.values()
    注意方法的返回值类型是字典，必须使用get方法通过键来查询值 
6 切片
    限制查询集，可以使用下标的方法进行限制
    左闭右开区间: 不支持负数
    下标没有负数: 实际上相当于 limit  offset
    
    studentList = Student.objects.all()[0:5]  
    第一个参数是offset  第二个参数是limit
    
    (1)缓存集：
        - 查询集的缓存：每个查询集都包含一个缓存，来最小化对数据库的访问;
        - 在新建的查询集中，缓存首次为空，
          第一次对查询集求值，会发生数据缓存，django会将查询出来的数据做一个缓存，并返回查询结果，
          以后的查询直接使用查询集的缓存。
        - 都不会真正的去查询数据库。

    (2)懒查询：
        - 只有我们在迭代结果集(for 循环遍历)，或者获取单个对象属性(student.name)的时候，它才会去查询数据
        - 为了优化我们结果和查询
```

```python
def testFilter1(request):
    # all
    # persons = Person.objects.all()
    # print(type(persons))
    # for person in persons:
    #     print(person.id,person.name,person.age)

    # filter
    # persons = Person.objects.filter(age__gt=20)
    # print(type(persons))
    # for person in persons:
    #     print(person.id,person.name,person.age)

    # exclude
    # persons = Person.objects.exclude(age__gt=20)
    # print(type(persons))
    # for person in persons:
    #     print(person.id,person.name,person.age)

    # order_by
    # 默认是升序
    # persons = Person.objects.order_by('age')
    # 降序
    # persons = Person.objects.order_by('-age')
    # print(type(persons))
    # for person in persons:
    #     print(person.id,person.name,person.age)

    # values
    # persons = Person.objects.values()
    # print(type(persons))
    # for person in persons:
    #     print(person['id'],person['name'],person['age'])

    # 切片
    # page  per_page
    # 1   0  5
    # 2   5  10

    # (page-1)*per_page:page*per_page

    persons = Person.objects.all()[5:10]
    print(type(persons))
    for person in persons:
        print(person.id,person.name,person.age)

    return HttpResponse('查询成功')
```

### 获取单个对象：

```tex
1 get
	- 不存在会抛异常  DoesNotExist
    - 存在多于一个    MultipleObjectsReturned
    - 使用这个函数    记得捕获异常
2 last
    - 返回查询集种的最后一个对象
3 first
    需要主动进行排序
    persons=Person.objects.all().first()
----------------------------------------
内置函数：框架自己封的方法 帮助我们来处理业务逻辑
4 count
	- 返回当前查询集中的对象个数
	- eg：登陆
5 exists
    - 判断查询集中是否有数据，如果有数据返回True没有反之
```

```python
def getOne(request):
    # get
    # person = Person.objects.get(pk=2)
    # print(type(person))
    # print(person.id,person.name,person.age)

    # last
    # person = Person.objects.last()
    # print(type(person))
    # print(person.id,person.name,person.age)

    # first
    # person = Person.objects.first()
    # print(type(person))
    # print(person.id,person.name,person.age)

    # count
    # person = Person.objects.filter(name='潘金莲').filter(age=20)
    #
    # if person.count()>0:
    #     print(111)
    # else:
    #     print(222)

    # exists
    # person = Person.objects.filter(name='潘金莲').filter(age=19)
    # # exists如果调用者中有数据  那么返回的就是True 如果没有数据 那么返回的就是False
    # if person.exists():
    #     print(111)
    # else:
    #     print(222)

    # 扩展get
    # get方法如果找不到对象那么Person matching query does not exist.
    # person = Person.objects.get(pk=100)
    # 如果get方法返回了多个值  那么报错MultipleObjectsReturned
    persons = Person.objects.get(age=18)

    return HttpResponse('查询成功')
```

### 字段查询：

```python
含义：对sql中where的实现，作为方法filter(),exclude(),get()的参数；
语法：属性名称__比较运算符=值
    Person.objects.filter(p_age__gt=18)
条件： 属性__操作符=临界值
    (1)gt  =>great than大于
    (2)gte =>great than equals大于等于
    (3)lt  =>less than小于
    (4)lte =>less than equals小于等于
    	filter(sage__gt=30)
    	
    (5)in：是否包含在范围内,filter(pk__in=[2,4,6,8])
    单引号可以使用
    (6)exact：判断，大小写不敏感，filter(isDelete = False)
    (7)startswtith
    	类似于 模糊查询 like
    (8)endswith
    	以 xx 结束  也是like
    (9)contains：是否包含，大小写敏感，filter(sname__contains='赵')
    (10)isnull,isnotnull：是否为空，filter(sname__isnull=False)
    (11)ignore 忽略大小写
        iexact
        icontains
        istartswith
        iendswith
        以上四个在运算符前加上 i(ignore)就不区分大小写了 iexact...
```

### 时间：

```python
# 模型定义
models.DateTimeField(auto_now_add=True)
	year
	month 会出现时区问题  需要在settings中设置：USE-TZ = False
	day
	week_day
	hour
	minute
	second
# 查询：
orders = Order.objects.filter(o_time__month=9)
# 有坑：时区问题
    关闭django项目下settings中自定义的时区
    	USE-TZ=False
    在数据库中创建对应的时区表
```

```python
def addOrder(request):
    order = Order()
    order.save()
    return HttpResponse('添加成功')


def getYear(request):
    order = Order.objects.filter(o_time__year='2020')[0]
    print(order.o_time)
    return HttpResponse('查询成功')


def getMonth(request):
    order = Order.objects.filter(o_time__month=8)[0]
    print(order.o_time)

    return HttpResponse('查询成功')
# ------------------------------
class Order(models.Model):
    o_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order'
```

### 聚合函数：

```tex
注意：mysql、oracle中所说的聚合函数、多行函数 、组函数 都是一个东西：max min avg sum count
聚合函数/组函数/多行函数/高级函数
1 模型：
class Customer(models.Model):
    c_name = models.CharField(max_length=16)
    c_cost = models.IntegerField(default=10)
2 使用：
    使用aggregate()函数返回聚合函数的值
        Avg：平均值
        Count：数量
        Max：最大
        Min：最小
        Sum：求和
    eg:Student.objects.aggregate(Max('age'))
```

```python
def testAggr(request):
    # Sum
    sum_cost = Custom.objects.aggregate(Sum('cost'))
    print(sum_cost)

    # Max
    max_cost = Custom.objects.aggregate(Max('cost'))
    print(max_cost)

    # Min
    min_cost = Custom.objects.aggregate(Min('cost'))
    print(min_cost)

    # Count
    count_cost = Custom.objects.aggregate(Count('cost'))
    print(count_cost)

    # Avg
    avg_cost = Custom.objects.aggregate(Avg('cost'))
    print(avg_cost)
    return HttpResponse('查询成功')
```

### 跨关系查询：

```python
跨关系查询:
	模型：
		class Grade(models.Model):
    		g_name = models.CharField(max_length=16)
        class Student(models.Model):
            s_name = models.CharField(max_length=16)
            s_grade = models.ForeignKey(Grade)
    使用：
        模型类名__属性名__比较运算符    实际上就是处理的数据库中的join
            Grade  ---> g_name      
            Student---> s_name  s_grade（外键）
        gf = Student.objects.filter(name='凤姐')
        print(gf[0].s_grade.name)
        查询jack所在的班级
        grades = Grade.objects.filter(student__s_name='Jack')
```

### F对象：

```python
F对象:常适用于表内属性的值的比较
	模型：
		class Company(models.Model):
              c_name = models.CharField(max_length=16)
              c_gril_num = models.IntegerField(default=5)
              c_boy_num = models.IntegerField(default=3)
	F：获取字段信息，通常用在模型的自我属性比较，支持算术运算
	eg:男生比女生少的公司
	companies = Company.objects.filter(c_boy_num__lt=F('c_gril_num'))
	eg:女生比男生多15个人
	companies = Company.objects.filter(c_boy_num__lt=F('c_gril_num')-15)
```

### Q对象：

```python
Q对象:常适用于逻辑运算 与或非
    支持逻辑运算：
            & 与
            | 或
            ~ 非
    年龄小于25：
    	Student.objects.filter(Q(sage__lt=25))
    男生人数多余5 女生人数多于10个：
        companies = Company.objects.filter(c_boy_num__gt=1).filter(c_gril_num__gt=5)
        companies = Company.objects.filter(Q(c_boy_num__gt=5)|Q(c_gril_num__gt=10)       
	年龄大于等于的：
		Student.objects.filter(~Q(sage__lt=25))
```

