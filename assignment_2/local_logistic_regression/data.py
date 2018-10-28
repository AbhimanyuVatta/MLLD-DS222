from __future__ import division
import re
import numpy as np
from collections import defaultdict
from nltk.corpus import stopwords
import h5py


def tokenize(document):
    values = document.split("\t")
    label=values[0].rstrip().split(",")
    words = re.sub("\d+", "", values[1].rsplit('"',1)[0].split('"',1)[1])
    regex = r'(\w*)'
    bow=re.findall(regex,words)
    while '' in bow:
        bow.remove('')
    bow=map(str.lower, bow)
    stop_words = set(stopwords.words('english'))
    bow = [w for w in bow if not w in stop_words]
    return bow, label

dy = defaultdict(int)
dz = defaultdict(int)
train_dir="/scratch/ds222-2017/assignment-1/DBPedia.full/full_train.txt"
#train_dir="/media/abhimanyu/ADI/MTech/Third SEM/MLLD/Assignment2-Logistic_Regression_with_Parameter_Server_DS222-master/Assignment2-Logistic-Regression-PS-DS222/codes/Part1_local_logistic/DBPedia.verysmall/verysmall/verysmall_train.txt"
filename_train = open(train_dir,"r") 
#lines = filename_train.readlines()[3:]

lines_train = filename_train.readlines()

for line in lines_train[3:]:
    bow, labels = tokenize(line)
    for word in bow:
        dy[word] += 1
        for label in labels:
            dz[label] += 1
	   
threshold_value=100

i=0
for key in list(dy.keys()):
    if dy[key] < threshold_value:
        del dy[key]
    i+=1
    
i=0
for la in dy.keys():
    dy[la]=i
    i=i+1

i=0
for lz in dz.keys():
    dz[lz]=i
    i=i+1

print(len(dy))
print(len(dz))
#print(dy)
#print(dz)

test_dir="/scratch/ds222-2017/assignment-1/DBPedia.full/full_test.txt"
#test_dir="/media/abhimanyu/ADI/MTech/Third SEM/MLLD/Assignment2-Logistic_Regression_with_Parameter_Server_DS222-master/Assignment2-Logistic-Regression-PS-DS222/codes/Part1_local_logistic/DBPedia.verysmall/verysmall/verysmall_test.txt"
filename_test = open(test_dir,"r") 
lines_test = filename_test.readlines()

train_words=np.zeros((len(lines_train),len(dy)),dtype=np.float32)
test_words=np.zeros((len(lines_test),len(dy)),dtype=np.float32)
train_labels=np.zeros((len(lines_train),len(dz)),dtype=np.float32)
test_labels=np.zeros((len(lines_test),len(dz)),dtype=np.float32)

i=0
for line in lines_test:
    bow_test, label_test = tokenize(line)
    #label=labelize(line)

    for l in label_test:
        test_labels[i,dz[l]]=1
    for w in bow_test:
        test_words[i,dy[w]]=1
    test_labels[i,:]=test_labels[i,:]/np.sum(test_labels[i,:])
    i=i+1
    


i=0
for line in lines_train:
    bow_train, label_train = tokenize(line)
    #label=labelize(line)

    for l in label_train:
        train_labels[i,dz[l]]=1
    for w in bow_train:
        train_words[i,dy[w]]=1
    train_labels[i,:]=train_labels[i,:]/np.sum(train_labels[i,:])
    i=i+1
    
print(np.sum(train_words[0,:]))
print(train_labels[0,:])
print(np.sum(test_words[0,:]))
print(test_labels[0,:])

np.save("train_labels",train_labels)
#np.save("train",train)
#np.save("test",test)
np.save("test_labels",test_labels)
h5f1 = h5py.File('train_words.h5', 'w')
h5f1.create_dataset('d1', data=train_words)
h5f2 = h5py.File('test_words.h5', 'w')
h5f2.create_dataset('d2', data=test_words)
h5f1.close()
h5f2.close()
