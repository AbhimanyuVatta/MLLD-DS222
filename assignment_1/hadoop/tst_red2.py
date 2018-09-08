#!/usr/bin/env python3

import sys
import math
import re
import io

prev_token = None
events_list = []

stopWords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', '(', ')','', ' ', '``', '@', '.', 'en', ',', '–', '[', ']'])

# Data structure to store parameters
cnt_tot_label = 0   # C(Y=ANY)
cnt_label = {}        # C(Y=label)++
len_vocab = 0
cnt_line = 0
cnt_label_anytoken = {}  # Y=y and X=ANY
tot_label_unique = 0
cnt_label_token = {}

# reading from cache dir
for line in open('cf'):
    line.strip()

    key, value = line.split("\t", 1)

    if key == "Y=ANY":
        cnt_tot_label = int(value)
        continue

    if key == 'len_vocab':
        len_vocab = int(value)
        continue

    if key == 'line_count':
        cnt_line = int(value)
        continue

    if "X=" not in key:
         _,label = key.split("=",1)
         cnt_label[label] = int(value)
         continue

    # Y=y and X=ANY
    label, _ = key.split("^", 1)
    _,label = label.split("=", 1)
    cnt_label_anytoken[label] = int(value)

tot_label_unique = len(cnt_label)

no_predict = 0
no_tot_docs = 0

m=1000
q_x = 1.0/len_vocab
q_y = 1.0/tot_label_unique

for line in sys.stdin:

    line = line.strip()

    token_curr, value = line.split("\t", 1)

    if prev_token == token_curr:
        events_list.append(value)
    else:
        if prev_token:
            events_sorted = sorted(events_list)
            _, labels = events_sorted[0].split(" ", 1)
            labels = labels.split(",")
            labels[-1] = labels[-1].strip()

            sentence = events_sorted[1].split()
            sentence[0] = sentence[0].strip("\"")
            sentence[-2] = sentence[-2].strip("\"@en")

            #for tok in sentence:
                # convert all tokens to lower case
                #tok = tok.lower()
                # strip punctuation marks and special characters
                #tok = re.sub('[^A-Za-z0-9]+', '', tok)

            all_tokens = [x for x in sentence if x not in stopWords]

            prob_y = {}

            cnt_label_token = {}
            for i in range(2, len(events_sorted)):
                # get token and cnt label list
                _, token, cnts = events_sorted[i].split(" ", 2)

                # print(cnts)
                for count_label in cnts.split():

                    # Get the cnt and label.
                    cnt, _, label = count_label.split("=", 2)

                    if label not in cnt_label_token:
                        cnt_label_token[label] ={}

                    cnt_label_token[label][token] = int(cnt)

            for label in cnt_label:
                prob_y[label] = math.log( (cnt_label[label]+m*q_y) / (cnt_tot_label+m) )
                for token in all_tokens:
                    if label in cnt_label_token and token in cnt_label_token[label]:
                        num = cnt_label_token[label][token] + m*q_x
                    else:
                        num = m*q_x
                    den = cnt_label_anytoken[label] + m
                    prob_y[label] += math.log(num/den)

            max_label = max(prob_y, key=prob_y.get)

            if max_label in labels:
                no_predict += 1

            print("{}\t{}".format(prev_token, max_label))
            print("{}\tGroud truth : {}".format(prev_token, labels))

        events_list = [value]
        prev_token = token_curr
        no_tot_docs += 1

if prev_token == token_curr:
    events_sorted = sorted(events_list)
    _, labels = events_sorted[0].split(" ", 1)
    labels = labels.split(",")
    labels[-1] = labels[-1].strip()

    sentence = events_sorted[1].split()
    sentence[0] = sentence[0].strip("\"")
    sentence[-2] = sentence[-2].strip("\"@en")

    #for tok in sentence:
        # convert all tokens to lower case
        #tok = tok.lower()
        # strip punctuation marks and special characters
        #tok = re.sub('[^A-Za-z0-9]+', '', tok)
    
    all_tokens = [x for x in sentence if x not in stopWords]

    prob_y = {}

    cnt_label_token = {}
    for i in range(2, len(events_sorted)):
        # token and cnt label list
        _, token, cnts = events_sorted[i].split(" ", 2)

        for count_label in cnts.split():

            #extract cnt and label
            cnt, _, label = count_label.split("=", 2)

            if label not in cnt_label_token:
                cnt_label_token[label] ={}

            cnt_label_token[label][token] = int(cnt)

    for label in cnt_label:
        prob_y[label] = math.log( (cnt_label[label]+m*q_y) / (cnt_tot_label+m) )
        for token in all_tokens:
            if label in cnt_label_token and token in cnt_label_token[label]:
                num = cnt_label_token[label][token] + m*q_x
            else:
                num = m*q_x
            den = cnt_label_anytoken[label] + m
            prob_y[label] += math.log(num/den)

    max_label = max(prob_y, key=prob_y.get)

    if max_label in labels:
        no_predict += 1

    print("{}\t{}".format(prev_token, max_label))
    print("{}\tGroud truth : {}".format(prev_token, labels))

print("Stats\t{} {}".format(no_predict, no_tot_docs))
