#!/usr/bin/env python3

import sys

for line in sys.stdin:

    line = line.strip()
    event, cnt = line.split('\t', 1)
    
    if 'X=' in event:
        attri = event.split("^", 1)
        all_tokens = attri[1].split("=", 1)

        print(all_tokens[1] +'\t'+ cnt + "=w^" + attri[0])




