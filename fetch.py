#!/usr/bin/env python3
# encoding: utf-8
import re

recordno = 0
column = 0
plan = {}

file = open("vplan-bsp.html",'r')
for line in file:
    result = re.search(r"<tr class='list (odd|even)'>", line)
    if result:
        recordno += 1
        column = -1
        plan[recordno] = {}
    
    result = re.search("color: #010101\">(.*)<", line)
    if result:
        column += 1
        plan[recordno][column] = result.groups(0)

print('FERTIG')
print(recordno)
print('-----')

for record in plan.items():
    print(record)
