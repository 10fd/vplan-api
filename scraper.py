#!/usr/bin/env python3
# encoding: utf-8
import regex
import requests
#from bs4 import BeautifulSoup

url_heute = 'http://extra.taunusgymnasium.de/vplan/f2/subst_001.htm'
url_morgen = 'http://extra.taunusgymnasium.de/vplan/f2/subst_001.htm'

def getWebContent(url):
    return requests.get(url).text

def getData(content):
    recordno = 0
    column = 0
    plan = {}

    for line in content:
        result = regex.search(r"<tr class='list (odd|even)'>", line)
        if result:
            recordno += 1
            column = -1
            plan[recordno] = {}
    
        result = regex.search("color: #010101\">(.*)<", line)
        if result:
            column += 1
            plan[recordno][column] = result.groups(0)

    print(recordno)

    for record in plan.items():
        print(record)

#webContent_soup = BeautifulSoup(getWebContent(url_heute), 'html.parser')
#print(webContent_soup)

getData(getWebContent(url_heute))
getData(getWebContent(url_morgen))
