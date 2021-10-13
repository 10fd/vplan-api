#!/usr/bin/env python3
# encoding: utf-8
import requests
from bs4 import BeautifulSoup

url = "http://extra.taunusgymnasium.de/vplan/f1/subst_001.htm"
web = requests.get(url)
soup = BeautifulSoup(web.content, "html.parser")

datum_A = soup.find("div" , class_="mon_title")

titleClass = soup.find_all("td" , class_= "titleColumn")

titles = []
for tag in titleClass:
  link = tag.find_all("a" , href = True)

  for tag in link:
    titles.append(tag.text)

ratingClass = soup.find_all("td" , class_="ratingColumn")

ratings = []
for tag in ratingClass:
  rating = tag.find_all("strong")

  for j in rating:
    ratings.append(float(j.text))
