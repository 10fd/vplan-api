#!/usr/bin/env python3
# encoding: utf-8
import flask
from flask import request, jsonify
import regex
import requests
import json

URL_HEUTE = 'http://extra.taunusgymnasium.de/vplan/f1/subst_001.htm'
URL_MORGEN = 'http://extra.taunusgymnasium.de/vplan/f2/subst_001.htm'

PARSER_REGEX = '((?:#.{6})\"(?:.{0,1})\>(?!<)(\&nbsp\;|.*?)(?:\<\/span\>){0,1}\<\/td\>){1}'

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def get_schedule(day):
    status = 'Routine nicht initialisiert'
    lookup = ''
    
    if day == 'heute':
        lookup = URL_HEUTE
    if day == 'morgen':
        lookup = URL_MORGEN
    if lookup == '':
        status = 'Tag nicht definiert'
    
    # (untested, da momentan nur "heute" und "morgen" zugelassen sind -- wird sich beim ersten Ausfall des Servers zeigen)
    try:
        content = requests.get(lookup).text
        
        if content:
            dictionary = {}
            entry = 0
            for line in content.splitlines():
                parsed = regex.findall(PARSER_REGEX, line, overlapped=False)
                
                if parsed:
                    entry += 1
                    dictionary[entry] = {}

                    itemcnt = 0
                    for items in parsed:
                        itemcnt += 1
                        
                        def dictvalue():
                            if items[1] == '&nbsp;' or items[1] == '---':
                                return ""
                            else:
                                return items[1]

                        if itemcnt == 1: 
                            dictionary[entry]["Stunde"] = dictvalue()
                        if itemcnt == 2:
                            dictionary[entry]["Klasse"] = dictvalue()
                        if itemcnt == 3:
                            dictionary[entry]["Fach"] = dictvalue()
                        if itemcnt == 4:
                            dictionary[entry]["Raum"] = dictvalue()
                        if itemcnt == 5:
                            dictionary[entry]["Vertretung"] = dictvalue()
                        if itemcnt == 6:
                            dictionary[entry]["Ver_Fach"] = dictvalue()
                        if itemcnt == 7:
                            dictionary[entry]["Art"] = dictvalue()

            status = json.dumps(dictionary)
 
    except requests.exceptions.RequestException as e:
        status = e
    
    result_json = {'status': status}
    return result_json

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Sinnlos</h1><p>Nutze die API-URL für den Stundenplan.</p>'''

@app.route('/api/v1/resources/stundenplan/heute', methods=['GET'])
@app.route('/api/v1/resources/stundenplan/morgen', methods=['GET'])
def api_all():
    day = request.path.split('/')[len(request.path.split('/'))-1:][0]
    return get_schedule(day)

app.run()
