# Headlines with Cookies
# https://github.com/Wasserratte/headlines.git
# Headlines

import datetime #1
import feedparser
from flask import Flask
import json
from flask import make_response #2
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


CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=6adcf9db3f524cffa0b639afa66142f8"


def get_value_with_fallback(key):   #7
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]




@app.route("/")         
    
def home():      

    # get customized headlines, based on user input or default (from home.html)

    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

   
    #get customized weather based on user input or default (from home.html)

    city = get_value_with_fallback("city")
    weather = get_weather(city)

    #get customized currency based on user input or default

    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    #save cookies and return template
    #3
    response = make_response(render_template("home.html",
                                             articles=articles,
                                             weather=weather,
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             currencies=sorted(currencies)))
    #4
    expires = datetime.datetime.now() + datetime.timedelta(days=365)

    #5
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)

    #6
    return response

  
                          

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


def get_rate(frm, to):      
    all_currency = urllib2.urlopen(CURRENCY_URL).read() #Load data over HTTP into a Python-String 

    parsed = json.loads(all_currency).get('rates')     # Parse a json-string into a Python-Dictionary
                                                       # .get() takes the key rates from the API and store
                                                       # this values in the Python-Dictionary parsed

    from_rate = parsed.get(frm.upper()) # parsed.get(frm.upper()) takes the values from the currency
                                        # according to the parameter of the get_rate() function e.g. USD

    to_rate = parsed.get(to.upper())    # parsed.get(to.upper()) takes the values from the currency
                                        # according to the get_rate() parameter e.g. EUR

                                        # parsed.get() takes the keys from the Python-Dictionary

    return (to_rate / from_rate, parsed.keys())  # parsed.key() is the list of the json value as Python-Dictionary.
                                                 # The parsed.keys() is the value for the currencies variable in the
                                                 # home function that is rendert sorted to the home.html to create the
                                                 # drop-down elements with all currencies from the json value


                                        
    


if __name__ == '__main__':
    app.run(port=5000, debug=True)
    

# Cookies are key-value pairs. When we use cookies we go through this steps:
# Set cookies--> Remember cookies--> Retriev user information, that are stored
#                                    in the cookies

#1) We'll use datetime library from Python to set the lifespan of our cookies

#2) Flask's make_response() function to create a response object that we can
#   set cookies on

##############################################################################
#                               Set cookies                                  #
##############################################################################

#   We create first the response object which stores the information which will be
#   rendered to the home.html template later.
#   This object will be used to set cookies which stores this userinformation
#   on the users computer.
#   Finally we return the entire response content-->render template and cookies

#3) We wrap a make_response() call around our render_template() call instead
#   of returning the rendered template directly. This means that our Jinja
#   templates will be rendered, and all the placeholders(user input values)
#   will be replaced with the correct values, but instead of returning
#   this response directly to our users, we will load it into a variable so that
#   we can make some more additions to it.

#4) 
#   Once we have this response object, we will create a datetime object with a
#   value of 365 days from today's date. So long will the cookie exist on the
#   users computer.

#5)
#   Then, we will do a series of set_cookie() calls on our response object,
#   saving all the user's selections(or refreshing the previous defaults) and
#   setting the expiry time to a year from the time the cookie was set using
#   our datetime object. A cookie is make up with the name of the cookie,
#   the user input value for this parameter and the expiry date.

#6)
#   Finally, we will return our response object, which contains the HTML for
#   the rendered template, and our four cookie values. On loading the page
#   our user's browser will save the four cookies, and we'll be able to retrieve
#   the values if the same user visits our application again.

################################################################################
#                               Retrieving cookies                             #
################################################################################

#   We nned to check for the saved cookies when a user sends us a request.

#   To retrieve the cookies values we use request.cookies.get()

#   Our logic for the user input:
#
#   We still want explicit request to take the highest priority. If no
#   explicit request is given we will look in the cookies to check wheather we
#   can grab a default from there. Finally, if we still have nothing, we will
#   use our hardcoded DEFAULTS.

#7) This function implements our fallback logic. This function is called
#   from the home() function.
