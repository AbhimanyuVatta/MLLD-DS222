export REDUCERS=2

hadoop dfs -rm -r /user/abhimanyuv/request

hadoop jar hadoop-streaming.jar -D mapred.reduce.tasks=$REDUCERS \
-file ./request_mapper.py -mapper ./request_mapper.py \
-file ./request_reducer.py -reducer ./request_reducer.py \
-input /user/ds222/assignment-1/DBPedia.verysmall/verysmall_test.txt,/user/abhimanyuv/word/ \
-output /user/abhimanyuv/request

# rm -rf request

# hadoop dfs -copyToLocal /user/abhimanyuv/request .


hadoop dfs -rm -r /user/abhimanyuv/test

hadoop jar hadoop-streaming.jar -D mapred.reduce.tasks=$REDUCERS \
-file ./test_mapper.py -mapper ./test_mapper.py \
-file ./test_reducer.py -reducer ./test_reducer.py \
-cacheFile './cache/part-00000#cf' \
-input /user/ds222/assignment-1/DBPedia.verysmall/verysmall_test.txt,/user/abhimanyuv/request  \
-output /user/abhimanyuv/test

rm -rf test

hadoop dfs -copyToLocal /user/abhimanyuv/test .

cp -rf test/ log_files
