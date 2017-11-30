# Render_template with GET-Request and Weather API, Currency Exchange Rate API
# https://github.com/Wasserratte/headlines.git
# Headlines

import feedparser
from flask import Flask
import json
from flask import render_template
from flask import request
import urllib 
import urllib2

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest',
            'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication':'bbc',   # If a request doesn't fit our code will fall back getting what it needs from there
            'city':'London,UK',
            'currency_from':'GBP',
            'currency_to':'USD'
            }

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=8b55a9ee343dcbbe22412e4aef9c9a12"

#1
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=6adcf9db3f524cffa0b639afa66142f8"

@app.route("/")         
    
def home():      

    # get customized headlines, based on user input or default (from home.html)

    publication = request.args.get('publication')

    if not publication:
        publication = DEFAULTS['publication']

    articles = get_news(publication)

    #get customized weather based on user input or default (from home.html)

    city = request.args.get('city')

    if not city:
        city = DEFAULTS['city']

    weather = get_weather(city)

    #get customized currency based on user input or default

    currency_from = request.args.get("currency_from") #3
    if not currency_from:
        currency_from = DEFAULTS['currency_from']

    currency_to = request.args.get("currency_to")   #4
    if not currency_to:
        currency_to = DEFAULTS['currency_to']

    rate = get_rate(currency_from, currency_to) #5

    return render_template("home.html", articles=articles, weather=weather,
                           currency_from=currency_from, currency_to=currency_to, rate=rate) #6

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:     
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed =feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):                
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None  #Define a Variable which will return later
    if parsed.get('weather'):
        weather = {'description':parsed['weather'] [0] ['description'],
                   'temperature':parsed['main'] ['temp'],
                   'city':parsed['name'],
                   'country': parsed['sys'] ['country']
                   }
    return weather


def get_rate(frm, to):      #2
    all_currency = urllib2.urlopen(CURRENCY_URL).read() #Load data over HTTP into a Python-String 

    parsed = json.loads(all_currency).get('rates')     # Parse a json-string into a Python-Dictionary
                                                       # .get() takes the key rates from the API and store
                                                       # this values in the Python-Dictionary parsed

    from_rate = parsed.get(frm.upper()) # parsed.get(frm.upper()) takes the values from the currency
                                        # according to the parameter of the get_rate() function e.g. USD

    to_rate = parsed.get(to.upper())    # parsed.get(to.upper()) takes the values from the currency
                                        # according to the get_rate() parameter e.g. EUR

                                        # parsed.get() takes the keys from the Python-Dictionary

    return to_rate/from_rate


                                        
    


if __name__ == '__main__':
    app.run(port=5000, debug=True)


#1) Add the variable CURRENCY_URL to the globals with the webadress for openexchangerates

#2) Add the get_rate() function to parse the information for the currencies

#3) In the variable currency_from we store the value of the input of the website. Name of the
#   parameter in request.args.get("currency_from") and the name in the html template has to be the same

#4) In the variable currency_to we store the value of the input of the website. Name of the parameter
#   in request.args.get("currency_to") and the name in the html template has to be the same.

#5) In the variable rate we store the return values of the get_rate() function. We put in the values of
#   the user input (currency_from and currency_to) as parameter for the function

#6) We render the neccassery values to the home.html template.
