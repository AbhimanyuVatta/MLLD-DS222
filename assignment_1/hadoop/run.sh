./train.sh 1 > log_files/bash_log 2>&1; ./test.sh 1 >> log_files/bash_log 2>&1
./train.sh 2 > log_files/2bash_log 2>&1; ./test.sh 2 >> log_files/2bash_log 2>&1
./train.sh 4 > log_files/4bash_log 2>&1; ./test.sh 4 >> log_files/4bash_log 2>&1
./train.sh 6 > log_files/6bash_log 2>&1; ./test.sh 6 >> log_files/6bash_log 2>&1
./train.sh 8 > log_files/8bash_log 2>&1; ./test.sh 8 >> log_files/8bash_log 2>&1
./train.sh 10 > log_files/10bash_log 2>&1; ./test.sh 10 >> log_files/10bash_log 2>&1