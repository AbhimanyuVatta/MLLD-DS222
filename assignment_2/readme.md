USAGE

Local Logistic Regression -
1. Prepare Data - run "python data.py" file in local_logistic_regression foldder to build h5py files for training and testing 
data provided in DBPedia dataset.
2. Constant Learning Rate(LR) -run "python lr const.py" to run Logistic Regression SGD with a constant learning rate.
3. Decreasing LR - run "python lr dec.py" to run Logistic Regression SGD with a decreasing learning rate per epoch.
4. Increasing LR - run "python lr inc.py" to run Logistic Regression SGD with a increasing learning rate per epoch.

Distributed Logistic Regression -
Data files used are the same created by running data.py program. Cluster IP addresses of parameter server and workers are coded
inside *.py files in distributed_logistic_regression folder and can be changed as required. Thereafter following commands need
to be run on respective cluster IP addresses of server and workers. Example given is for bulk synchronous model program for a 
single parameter server and two worker nodes. However, more worker nodes may also be defined.

1. python bulksync.py –job name=”ps” --task index=0 (on server IP) 
3. python bulksync.py –job name=”worker” --task index=0 (on first worker IP as given inside *.py file)
4. python bulksync.py –job name=”worker” --task index=1 (on second worker IP as given inside *.py file).
