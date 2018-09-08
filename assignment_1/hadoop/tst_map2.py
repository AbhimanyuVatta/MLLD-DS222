#!/usr/bin/env python3

import sys

prev_word = None


for line in sys.stdin:
    line = line.strip()
    
    key, value = line.split("\t", 1)

    # Print id counts
    if "~ctr_for" in value:
        print(line)
        continue

    labels, data = line.split("\t", 1)

    attri = data.split(" ", 2)
    # print(line)
    print("{}\t~a_label {}".format(attri[0], labels))
    print("{}\t~b_data {}".format(attri[0], attri[2]))

