#!/usr/bin/env python

import re

##
# note the different approach to various parts of your regex
##
pattern = re.compile(r'''(\w+\s\d+\s\d+:\d+:\d+).+SRC=([\d.]+)\s+DST=([\d.]+)\s+(?:.*?TCP|UDP)\s+SPT=(\d+)\s+DPT=(\d+)\s+SEQ=(\d+)\s+ACK=(\d+)''')

def time2sec(my_time):
    my_time = my_time.split(":")
    return int(my_time[2]) + int(my_time[1]) * 60 + \
           int(my_time[0]) * 360

# let's use a dictionary of requests
requests = {}

my_file = open('source.log')
for line in my_file.xreadlines():
    match = pattern.search(line)
    if not match: continue

    date     = match.group(1)
    src_addr = match.group(2)
    dst_addr = match.group(3)
    src_port = int(match.group(4))
    dst_port = int(match.group(5))
    seq      = match.group(6)      # seq and ack are too big for int, they
    ack      = match.group(7)      # need long, so i left them as strings

    print match.groups()           # for debugging

    if src_port > 1024 and long(ack) == 0:
        # the final zero will be used to keep a running tally of time spent
        # which is why I use a list and not a tuple here
        requests[seq] = [date, src_addr, dst_addr, src_port, dst_port, 0]
    elif requests.has_key(ack) and \
         dst_port == requests[ack][3] and src_port == requests[ack][4] and \
         dst_addr == requests[ack][1] and src_addr == requests[ack][2]:
        # the above check is very pedantic to ensure we are using the
        # correct request
        t1 = time2sec(requests[ack][0])
        t2 = time2sec(date)
        requests[ack][5] += t2 - t1
    # needs an else to catch what the above to miss, I do not understand
    # the problem well enough to write it

my_file.close()

for key in requests.keys():
    print requests[key][1], requests[key][5]
