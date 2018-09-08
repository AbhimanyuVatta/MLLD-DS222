#!/usr/bin/env python3

import sys

prev_token = None
token_values = []

for line in sys.stdin:

    line = line.strip()
    
    token, value = line.split("\t", 1)
    
    if prev_token == token:
        token_values.append(value)
    else:
        if prev_token:
            token_values_sorted = sorted(token_values)
            if "=w^Y=" in token_values_sorted[0]:
                for i in range(1, len(token_values_sorted)):
                    _, Id = token_values_sorted[i].split()
                    print("{}\t~ctr_for {} {}".format(Id, prev_token, token_values_sorted[0]))
        token_values = [value]
        prev_token = token

if prev_token == token:
    token_values_sorted = sorted(token_values)
    if "=w^Y=" in token_values_sorted[0]:
        for i in range(1, len(token_values_sorted)):
            _, Id = token_values_sorted[i].split()
            print("{}\t~ctr_for {} {}".format(Id, prev_token, token_values_sorted[0]))

