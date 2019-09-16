source加载 .

## 一、Shell脚本概述

> 通过Shell中的各种命令，开发者和运维人员可以对服务器进行维护工作。
>
> 但每次都手动输入命令，工作效率太低，而且容易出错，尤其是需要维护大量服务器时。
>
> 为了能够对服务器批量执行操作，我们可以将需要执行的命令写入文件，批量执行，这种文件便是Shell脚本。

Shell脚本一般是一`.sh`结尾的文本文件，可以省略扩展名。

## 二、Shell脚本运行

> 第一行通过注释的方式指明执行脚本的程序。

> 在Shell脚本中，`#`是注释，`#!`开头的这一行代码告诉Shell使用哪个程序来执行当前脚本。

如：

* `#!/bin/sh`
* `#!/bin/bash`
* `#!/usr/bin/env bash`

python脚本的第一句：`#!/usr/bin/env python`

执行：`python test.py`

## 三、第一个脚本

1. 创建test.sh文件

2. 将下面文本写入到test.sh中

   ```sql
   #!/bin/bash
   
   echo "Hello"
   echo "I am `whoami`"
   echo "I love Linux"
   echo "The CPU in my PC has `cat /proc/cpuinfo |grep -c processor` cores"
   exit 0
   ```

3. 执行`chmod a+x test.sh`对脚本授予可执行权限或`chmod 755 test.sh`文件创建时默认权限 644；

4. 输入`./test.sh`执行脚本或`source ./test.sh `加载资源后执行 。

5. 查看脚本的执行状态码：`echo $?`

   * Linux中所有程序执行结束后都有状态码
   * 状态码为`0`**表示正常**，为`1、2...`正整数**代表异常退出**

## 四、变量

* 1.定义：**注意赋值前后没有空格**

```shell
# 变量定义：等号前后没有空格
a=123
b=xyz
```

* 2.使用变量时，变量名前面加上`$`符

```shell
echo -e "---$a---\n===$b==="
printf "---$a---\n===$b===\n"末尾不加\n会挤出光标
```

* 3.注意 **引号** 的区别

```shell
echo 'it is a $a' #无效输出
echo "it is a $a" #变量输出必须使用双引号
```

* 4.**export**定义当前Shell下的**全局变量**
  * 定义：`export A=123`
  * 定义完后，在终端里用source加载脚本：`source ./test.sh`

* 5.常用的系统环境变量
  * $PATH：可执行文件目录
  * $PWD：当前目录
  * $HOME：家目录
  * $USER：当前用户名
  * $UID：当前用户的uid



## 五、分支语句

分支控制语句格式为：

```shell
if command
then 
	commands;
elif command
then
	commands;
else 
	commands;
fi;
```

* 1.if语句检查判断的依据实际上是，后面所跟命令的状态码：**0为true，其他为fasle**

```shell
if ls /xxx
then
	echo "exist xxx"
else
	echo "not exist xxx"
fi
```

* 2.条件测试命令：`[ ... ]`

  * shell提供了一种专用做条件测试的语句[ ... ]

  * 这一方括号本质是一个命令，这里面的条件是其参数，所以**[  的后面  ]的前面必须有空格**，否则会报错。

  * 它可以进行三种比较
    * 数值比较
    * 字符串比较
    * 文件比较

* 用法：

  ```shell
  if [ conditions ]
  then
  	commands
  fi
  ```


* 3.条件列表

  数值比较：**运算符两边一定要有空格**

| Condition | 说明                 |
| --------- | -------------------- |
| m -eq n   | 检查m是否与n相等     |
| m -ge n   | 检查m是否大于或等于n |
| m -gt n   | 检查m是否大于n       |
| m -le n   | 检查m是否小于或等于n |
| m -lt n   | 检查m是否小于n       |
| m -ne n   | 检查m是否不等于n     |

​    字符串比较：**运算符两边一定要有空格**

| condition     | 说明                                                         |
| ------------- | ------------------------------------------------------------ |
| str1 = str2   | 检查str1是否等于str2                                         |
| str1 != str2  | 检查str1是否不等于str2                                       |
| str1 \\> str2 | 检查str1是否大于str2(单个>表示重定向，或者使用 [[ str1 > str2 ]] ) |
| str1 \\<str2  | 检查str1是否小于str2                                         |
| -n str1       | 检查str1的长度是否 **非0**                                   |
| -z str1       | 检查str1的长度是否 **为0**                                   |

```shell
a='abc'
b='qwer'
[ $a = $b ]; echo $?
[ -n $a ]; echo $?
[ -z $a ]; echo $?
b=''
[ -z $b ]; echo $?

```

​     **文件比较**

| Condition       | 说明                                   |
| --------------- | -------------------------------------- |
| -d file         | 检查file是否存在并是且是一个目录       |
| -e file         | 检查file是否存在                       |
| -f file         | 检查file是否存在并且是一个文件         |
| -r file         | 检查file是否存在并且可读               |
| -w file         | 检查file是否存在并且可写               |
| -x file         | 检查file是否存在并且可执行             |
| -s file         | 检查file是否存在并且非空               |
| -O file         | 检查file是否存在并且属当前用户所拥有的 |
| file1 -nt file2 | 检查file1是否比file2新                 |
| file1 -ot file2 | 检查file1是否比file2旧                 |

## 六、循环语句for

Shell中的循环结构有三种：`for`、`while`、`until`,重点介绍`for`循环

1.for循环的基本格式：

```shell
for 变量 in 序列
do
	要执行的命令
done
```

2.练习：打印 1 到 10 中的偶数

```shell
# `seq 1 10` 产生 1到10 的整数，类似Python的range函数
for i in `seq 1 10`
do
	if [[ $[ $i %2 ] == 0 ]]
	then
		echo "偶数：$i";
	else
		echo "奇数：$i";
	fi;
done
```

1. `seq START END`语句用来产生一个数字序列
2. `$[ NUM1 + NUM2]`语句用来进行基本的数学运算
3. `[[ ... ]]`语句用来更方便的进行比较判断

3.C语言风格的for循环

```shell
for ((i=0; i<5; i++))
do
	echo "num is $i"
done
```

## 七、函数

1.函数定义

定义时`function`不是必须的，可以省略

```shell
function foo() {
	echo "---------------------------"
	echo "Hello $1, nice to meet you!"
	echo "---------------------------"
}
# 终端调用
source test.sh
foo

. test.sh 等价于 source test.sh
foo
```

```shell
function foo() {
 
    echo "参数 0 : $0" #终端调用bash   #脚本调用是文件名
    echo "第1个参数 $1"
 	echo "第2个参数 $2"
	echo "第3个参数 $3"

	echo "全部的参数: $*"
	echo "全部的参数: $@"
 
    echo "一共有 $# 个参数"
}

# 终端调用
. test.sh
foo aa bb cc dd ee ff gg

# 脚本调用
# 如果脚本文件中已经调用了foo,则直接运行
./test.sh aa bb cc dd ee ff gg
```

2.函数的使用

* 在终端或脚本中直接输入函数名,不需要小括号

* 传参也只需将参数加到函数名后面,以空格做间隔

  ```tex
  foo arg1 arg2 ...
  ```

3.函数的参数

```shell
function bar() {
    echo "执行者是 $0"
    echo "参数量是 $#"
    echo "全部的参数 $@"
    echo "全部的参数 $*"
    if [ -d $1 ]; then ## 检查传入的第一个参数是否是文件夹
        for f in `ls $1`
        do
            echo $f
        done
    elif [ -f $1 ]; then
        echo 'This is a file: $1' # 单引号内的变量不会被识别
        echo "This is a file: $1" # 如果不是文件夹, 直接显示文件名
    else
        echo 'not valid' #前面都不匹配显示默认语句
    fi
}
```

## 八、read获取用户输入

```shell
read -p "请输入一个数字:" num
echo "您输入的是:$num"
```



