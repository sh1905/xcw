for i in `seq 1 10`
do
    if [[ $[ $i %2] == 0 ]]
    then
        echo "偶数：$i";
    else
        echo "奇数：$i";
    fi;
done
