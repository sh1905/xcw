#!/bin/bash

#for i in `seq 1 10`
#do
#    if [[ $[$i % 2] == 0  ]]
#    then
#        echo "这是一个偶数：$i";
#    else
#        echo "这是一个奇数：$i";
#    fi;
#done


function foo(){

    echo "参数0：$0"
    echo "第一个参数 $1"
    echo "第二个参数 $2"
    echo "第三个参数 $3"
    #echo 'i am foo'
    echo "全部的参数：$*"
    echo "全部的参数：$@"

    echo "一共有 $# 个参数"
}
foo xxx yyy zzz

echo "参数0：$0"
    echo "第一个参数 $1"
    echo "第二个参数 $2"
    echo "第三个参数 $3"
    #echo 'i am foo'
    echo "全部的参数：$*"
    echo "全部的参数：$@"
    echo "一共有 $# 个参数"



#echo "hello"
#echo "I am `whoami`"
#echo "I love Linux"
#echo "The CPU in my PC has `cat /proc/cpuinfo |grep -c processor` cores"
#exit 0


read -p "请输入一个数字：" num
echo "您输入的是：$num"
