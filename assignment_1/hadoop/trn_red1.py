#!/usr/bin/env python3

import sys
import io

prev_token = None
cnt_token_tot = 0
token = None

prev_lv_token = 'a'
len_vocab = 0

for line in sys.stdin:

    line = line.strip()

    token, value = line.split('\t', 1)

    # vocabulary length
    if value == 'len_vocab':
        if prev_lv_token != token:
            len_vocab += 1
            prev_lv_token = token
        continue

    cnt_token = int(value)

    if prev_token == token:
        cnt_token_tot += cnt_token
    else:
        if prev_token:
            print('{}\t{}'.format(prev_token, cnt_token_tot))
        prev_token = token
        cnt_token_tot = cnt_token

# OUTPUT last token.
if prev_token == token:
    print('{}\t{}'.format(prev_token, cnt_token_tot))

print("len_vocab\t{}".format(len_vocab))
