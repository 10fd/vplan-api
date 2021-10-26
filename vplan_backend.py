import flask
from flask import request, jsonify
import regex
import requests
import json

URL_HEUTE = 'http://extra.taunusgymnasium.de/vplan/f1/subst_001.htm'
URL_MORGEN = 'http://extra.taunusgymnasium.de/vplan/f2/subst_001.htm'

PARSER_REGEX = '010101\"\>(.*)\<\/span\>.*010101\"\>(.*)\<\/span\>.*010101\"\>(.*)\<\/span\>.*010101\"\>(.*)\<\/span\>.*010101\"\>(.*)\<\/span\>.*010101\"\>(.*)\<\/span\>.*010101\"\>(.*)\<\/span\>.*'

app = flask.Flask(__name__)
app.config["DEBUG"] = True # hier kann mit viel Bla in der Konsole abstellen

# Vertretungsplan bei jedem API-Call abrufen
def get_schedule(day):
    status = 'Routine nicht initialisiert'
    lookup = ''
    
    if day == 'heute':
        lookup = URL_HEUTE
    if day == 'morgen':
        lookup = URL_MORGEN
    if lookup == '':
        status = 'Tag nicht definiert'
    
    # hier wird der Stundenplan abgerufen
    # falls es beim Stundenplan-Server einen Fehler gibt, wird die Meldung in den Status weitergereicht
    # (untested, da momentan nur "heute" und "morgen" zugelassen sind -- wird sich beim ersten Ausfall des Servers zeigen)
    try:
        content = requests.get(lookup).text
        
        # nur machen, wenn etwas drin steht
        if content:
            dictionary = {}
            entry = 0
            for line in content.splitlines():
                parsed = regex.search(PARSER_REGEX, line)
                # nur wenn der lange Regex gematcht wird:
                if parsed:
                    entry += 1
                    dictionary[entry] = {}
                    dictionary[entry]["Stunde"]   = parsed.group(1)
                    dictionary[entry]["Klasse"]   = parsed.group(2)
                    dictionary[entry]["Fach"]     = parsed.group(3)
                    dictionary[entry]["Raum"]     = parsed.group(4)
                    dictionary[entry]["Vertretung"] = parsed.group(5)
                    dictionary[entry]["Ver_Fach"] = parsed.group(6)
                    dictionary[entry]["Art"]      = parsed.group(7)                   
                    status = json.dumps(dictionary)
 
    except requests.exceptions.RequestException as e:
        status = e
    
    # Anmerkung: der lange result_json sieht im Browser komisch aus. Am besten mal per print() in der Konsole anschauen
    result_json = {'status': status}
    return result_json

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Sinnlos</h1><p>Nutze die API-URL für den Stundenplan.</p>'''

# API-Endpoints definieren, letztes Element als Tag deklarieren und nachschauen
@app.route('/api/v1/resources/stundenplan/heute', methods=['GET'])
@app.route('/api/v1/resources/stundenplan/morgen', methods=['GET'])
def api_all():
    day = request.path.split('/')[len(request.path.split('/'))-1:][0]
    return get_schedule(day)

app.run()