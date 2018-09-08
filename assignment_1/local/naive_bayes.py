import os
import json
import math
import time
from nltk.corpus import stopwords
import codecs
import pickle

#size_type = 'verysmall'
size_type = 'full'

#data_files = {"verysmall":"/scratch/ds222-2017/assignment-1/DBPedia.verysmall/",
#        "full":"/scratch/ds222-2017/assignment-1/DBPedia.full/"}

data_files = {"verysmall":"/home/abhimanyuv/test/",
        "full":"/scratch/ds222-2017/assignment-1/DBPedia.full/"}

data_type = ['train', 'test', 'devel']

stop_words = set(stopwords.words('english'))
stop_words_extra = set(['(', ')','', ' ', '``', '@', '.', 'en', ',', '-', '[', ']'])
stop_words.update(stop_words_extra)

if not os.path.isdir('data'):
    os.mkdir('data')

if not os.path.isdir('data/'+size_type):
    os.mkdir('data/'+size_type)

if not os.path.isdir('models'):
    os.mkdir('models')
    
    
def readFile(path, data_type):
    
    with codecs.open(path + size_type +'_' + data_type + '.txt', encoding='unicode_escape', errors='ignore') as f:
        data = []
        count=0
        for line in f:

            # Skip the first three lines
            if count <3 and size_type == 'verysmall':
                count += 1
                continue

            sents = line.split("\t")

            labels = sents[0].split(",")
            labels[-1] = labels[-1].strip()
            sentence_temp = sents[1].split(" ", 2)

            # Split data based on space and remove stop words
            all_tokens = []
            sentence = sentence_temp[2].split()
            sentence[0] = sentence[0].strip("\"")
            sentence[-2] = sentence[-2].strip("\"@en")

            all_tokens = [token for token in sentence if token not in stop_words]
            
            # Add label data pair to data.
            data += [(labels, all_tokens)]

            count += 1

        return data


def write_all_data():
    for d_type in data_type:
        data = readFile(data_files[size_type], d_type)
        # Save the data
        with open('data/' + size_type + '/' + d_type + '.json', "w") as f:
            json.dump(data, f)
        with open('data/' + size_type + '/' + d_type + '.pkl', "wb") as f:
            pickle.dump(data, f)


def train():

    print("Training")
    
    st_time = time.time()

    data = readFile(data_files[size_type], 'train')

    
    # Data structure to store parameters
    cnt_tot_label = 0   # C(Y=ANY)
    cnt_label = {}        # C(Y=label)++
    cnt_label_token = {}    # Y=y and X=x
    cnt_label_anytoken = {}  # Y=y and X=ANY
    vocab = set()
    labels_unique = set()


    for labels, all_tokens in data:
        
        for label in labels:
            labels_unique.add(label)
            cnt_tot_label +=1   # C(Y=ANY)
            if label not in cnt_label:    # C(Y=label)++
                cnt_label[label] = 0
                cnt_label_token[label] = {}
                cnt_label_anytoken[label] = 0
            cnt_label[label] += 1

            for token in all_tokens:
                # C(Y=labe AND X=token)
                vocab.add(token)
                cnt_token = 0
                if token in cnt_label_token[label]:
                    cnt_token = cnt_label_token[label][token]
                cnt_token += 1
                cnt_label_token[label][token] = cnt_token

                cnt_label_anytoken[label] += 1    # C(Y=label AND X=ANY)

    en_time = time.time() - st_time
    print("Time for training {}".format(en_time))

    naive_bayes_data = {'cnt_tot_label' : cnt_tot_label,
                        'cnt_label' : cnt_label,
                        'cnt_label_token' : cnt_label_token,
                        'cnt_label_anytoken' : cnt_label_anytoken,
                        'len_vocab' : len(vocab),
                        'labels_unique' : list(labels_unique)}

    with open('models/naive_bayes_data.json', 'w') as f:
        json.dump(naive_bayes_data, f)

    print()

    return naive_bayes_data
    

def get_model():
    with open('models/naive_bayes_data.json', 'r') as f:
        return json.load(f)

def test_dev(set_type, nb=None, m=100):
    
    if not nb:
        nb = get_model()

    #print("Validating ")
    if set_type == 'devel':
        print('Development')
    else:
        print('Testing')
        
    st_time = time.time()

    data = readFile(data_files[size_type], set_type)

    correct = 0;
    prob_y = {}
    # m = 1

    cnt_tot_label = nb['cnt_tot_label']
    cnt_label = nb['cnt_label']

    cnt_label_token = nb['cnt_label_token'] 
    cnt_label_anytoken = nb['cnt_label_anytoken']

    len_v = nb['len_vocab']
    labels_unique = nb['labels_unique']

    q_x = 1.0 / len_v
    q_y = 1.0 / len(labels_unique)
    
    # print(data[:4])
    for labels, all_tokens in data:
        for label in labels_unique:
            prob_y[label] = math.log( (cnt_label[label]+m*q_y) ) - math.log( (cnt_tot_label+m) )
            for token in all_tokens:
                if token in cnt_label_token[label]:
                    num = cnt_label_token[label][token] + m*q_x
                else:
                    num = m*q_x
                den = cnt_label_anytoken[label] + m
                prob_y[label] += (math.log(num) - math.log(den))
        max_label = max(prob_y, key=prob_y.get)

        if max_label in labels:
            correct +=1
    en_time = time.time() - st_time

    print("Time for Validating {}".format(en_time))
    print("Accuracy {:.4f}".format(correct/len(data)))
    print()
    return correct/len(data)


def cnt_param():
    nb = get_model()
    cnt_tot_label = nb['cnt_tot_label']
    cnt_label = nb['cnt_label']

    cnt_label_token = nb['cnt_label_token'] 
    cnt_label_anytoken = nb['cnt_label_anytoken']

    #len_v = nb['len_vocab']
    labels_unique = nb['labels_unique']

    cnt_tot_param = 1

    cnt_label_param = len(cnt_label)
    cnt_tot_param += cnt_label_param

    cnt_label_token_param = 0
    
    for label in cnt_label_anytoken:
        cnt_label_token_param += len(cnt_label_token[label])
    cnt_tot_param += cnt_label_token_param

    cnt_label_anytoken_param = len(cnt_label_anytoken)
    cnt_tot_param += cnt_label_anytoken_param

    cnt_unq_label_param = len(labels_unique)

    print("Param count for C(Y=label) " + str(cnt_label_param))
    print("Param count for Y=y and X=x " + str(cnt_label_token_param))
    print("Param count for Y=y and X=ANY " + str(cnt_label_anytoken_param))
    print("Number of dom labels " +str(cnt_unq_label_param))
    print("Total param count " + str(cnt_tot_param))
    print('cnt_tot_label ' + str(cnt_tot_label))


if __name__ == "__main__":
    
    write_all_data()
    
    nb = train()

    test_dev('devel', nb, 100)

    test_dev('test', nb, 100)

    cnt_param()
