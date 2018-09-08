#!/usr/bin/env python3

import sys

prev_token = None
token_event = ''

# STDIN input
for line in sys.stdin:
    
    line = line.strip()

    token, cnt_token = line.split("\t", 1)
    
    if prev_token == token:
        token_event += " " + cnt_token
    else:
        if prev_token:
            print("{}\t{}".format(prev_token, token_event))
        token_event = cnt_token
        prev_token = token

if prev_token == token:
    print("{}\t{}".format(prev_token, token_event))
