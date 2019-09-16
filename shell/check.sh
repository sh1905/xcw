#!/bin/bash
read -p '请输入第一个文件名：' file1
read -p '请输入第二个文件名：' file2
code1=`md5sum $file1 |awk '{print $1}'`
code2=`md5sum $file2 |awk '{print $1}'`
if [ $code1 = $code2  ]
then
    echo "它们是同一个文件！";
else
    echo "它们不是同一个文件！";
fi;
