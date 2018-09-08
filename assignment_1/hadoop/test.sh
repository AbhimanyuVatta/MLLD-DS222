export REDUCERS=$1

hadoop dfs -rm -r /user/abhimanyuv/request

hadoop jar hadoop-streaming.jar -D mapred.reduce.tasks=$REDUCERS \
-file ./tst_map1.py -mapper ./tst_map1.py \
-file ./tst_red1.py -reducer ./tst_red1.py \
-input /user/ds222/assignment-1/DBPedia.full/full_test.txt,/user/abhimanyuv/word/ \
 -output /user/abhimanyuv/request

# rm -rf request

# hadoop dfs -copyToLocal /user/abhimanyuv/request .


hadoop dfs -rm -r /user/abhimanyuv/test

hadoop jar hadoop-streaming.jar -D mapred.reduce.tasks=$REDUCERS \
-file ./tst_map2.py -mapper ./tst_map2.py \
-file ./tst_red2.py -reducer ./tst_red2.py \
-cacheFile './cache/part-00000#cf' \
-input /user/ds222/assignment-1/DBPedia.full/full_test.txt,/user/abhimanyuv/request  \
 -output /user/abhimanyuv/test

rm -rf test/*

hadoop dfs -copyToLocal /user/abhimanyuv/test .

cp -rf test/ log_files/$REDUCERS
