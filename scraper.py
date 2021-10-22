#!/usr/bin/env python3
# encoding: utf-8
import regex
import requests

url_heute = 'http://extra.taunusgymnasium.de/vplan/f1/subst_001.htm'
url_morgen = 'http://extra.taunusgymnasium.de/vplan/f2/subst_001.htm'

def getWebContent(url):
    return requests.get(url).text

def getData(content):
    recordno = 0
    column = 0
    plan = {}

    for str in content.splitlines():
        result = regex.search(r"<tr class='list (odd|even)'>", str)
        if result:
            recordno += 1
            column = -1
            plan[recordno] = {}
    
        result = regex.search(r"color: #010101\">(.*?)<", str)
        if result:
            column += 1
            plan[recordno][column] = result.groups(0)

    for record in plan.items():
        print(record)

getData(getWebContent(url_heute))
getData(getWebContent(url_morgen))
