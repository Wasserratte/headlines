# Render_template with GET-Request and Weather API
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
            'city':'London,UK'}

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=8b55a9ee343dcbbe22412e4aef9c9a12'   

@app.route("/")         
    
def home():    #1  

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

    return render_template("home.html", articles=articles, weather=weather)

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:     #2
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed =feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):                 #3
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None  #Define a Variable which will return later
    if parsed.get('weather'):
        weather = {'description':parsed['weather'] [0] ['description'],
                   'temperature':parsed['main'] ['temp'],
                   'city':parsed['name']
                   }
    return weather
        
    


if __name__ == '__main__':
    app.run(port=5000, debug=True)


#1) The home function collects the user input with the request.args.get() method. This is stored in
#   the variable publication for the news and city for the weather. If no input is given the code
#   will take the DEFAULT-Parameters. The home function gives the parameter to the functions for the
#   news and weather. At the end of the function it transfers the parameter to the home.html to display it.

#2) The function get_news(query) parses the RSS-Feed (query = parameter home function)
#   It returns the feed parameter to the articles variable in the home function.


#3) The princible is the same as in the get_news() function.
#   The WEATHER_URL is the URL to get the API
#   urllib.quote(query) (query is the parameter from the home function) enables that we can use spaces in
#   city names e.g. New York.
#   WEATHER_URL.format and urllib2 loads data over HTTP into a Python-String by using urllib2.
#   json.loads convert json string into a Python-Dictionary.
#   The last part built up a simpler Python dictionary. if parsed.get("weather") takes weather from the API
