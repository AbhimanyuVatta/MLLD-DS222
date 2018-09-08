#!/usr/bin/env python3

import sys
import re

stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', '(', ')','', ' ', '``', '@', '.', 'en', ',', '–', '[', ']'])


for line in sys.stdin:

    line = line.strip()

    if 'Y=' in line:
        print(line)
        continue

    _, data = line.split('\t', 1)

    Id, _, all_tokens = data.split(" ", 2)

    all_tokens = all_tokens.split(" ")
    all_tokens[0] = all_tokens[0].strip("\"")
    all_tokens[-2] = all_tokens[-2].strip("\"@en")
    # all_tokens = re.split("\W+", all_tokens)

    for token in all_tokens:
        # convert all tokens to lower case
        #token = token.lower()
        # strip punctuation marks and special characters
        #token = re.sub('[^A-Za-z0-9]+', '', token)
        if token not in stopwords:
            print("{}\t~ctr_to {}".format(token, Id))

