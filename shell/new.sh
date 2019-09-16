#!/bin/bash

#function bar(){
#
#    echo "执行这时$0"
#    echo "参数量是$#"
#    echo "全部的参数$@"
#    echo "全部的参数$*"
#
#    if [ -d $1 ]; then
#        for f in `ls $1`
#        do
#            echo $f
#        done
#    elif [ -f $1 ];then
#        echo 'this is a file: $1'
#        echo "this is a file: $1"
#    fi
#
#}
for ((i=0;i<5;i++ ))
do
    echo "num is $i"
done
export A=666
