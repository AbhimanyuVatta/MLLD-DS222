export REDUCERS=$1

hadoop dfs -rm -r /user/abhimanyuv/event_counts

hadoop jar hadoop-streaming.jar -D mapred.reduce.tasks=$REDUCERS \
-file ./trn_map1.py -mapper ./trn_map1.py \
-file ./trn_red1.py -reducer ./trn_red1.py \
-input /user/ds222/assignment-1/DBPedia.full/full_train.txt \
-output /user/abhimanyuv/event_counts

# rm -rf event_counts

# # hadoop dfs -copyToLocal /user/abhimanyuv/event_counts .


# # # ################### Count by Word ###################

hadoop dfs -rm -r /user/abhimanyuv/word

hadoop jar hadoop-streaming.jar -D mapred.reduce.tasks=$REDUCERS \
-file ./trn_map2.py -mapper ./trn_map2.py \
-file ./trn_red2.py -reducer ./trn_red2.py \
-input /user/abhimanyuv/event_counts/ -output /user/abhimanyuv/word

# rm -rf word

# hadoop dfs -copyToLocal /user/abhimanyuv/word .

################### Create cache ###################


hadoop dfs -rm -r /user/abhimanyuv/cache

hadoop jar hadoop-streaming.jar \
-file ./trn_map3.py -mapper ./trn_map3.py \
-file ./trn_red3.py -reducer ./trn_red3.py \
-input /user/abhimanyuv/event_counts -output /user/abhimanyuv/cache

# rm -rf cache

# hadoop dfs -copyToLocal /user/abhimanyuv/cache .
