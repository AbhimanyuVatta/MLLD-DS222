#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.strip()
    
    key, cnt = line.split("\t", 1)

    if key == 'len_vocab':
        print(line)

    if key == 'line_count':
        print(line)


    if "X=ANY" in key:
        print(line)

    if "Y=" in key and "X=" not in key:
        print(line)
