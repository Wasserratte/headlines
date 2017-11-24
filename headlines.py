# Dynamic Routing
# https://github.com/Wasserratte/headlines.git
# Headlines

import feedparser 
from flask import Flask

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest',
            'iol': 'http://www.iol.co.za/cmlink/1.640'}         

@app.route("/")         #1
@app.route("/<publication>")    #2
def get_news(publication="bbc"):      
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'] [0]
    return """<html>
        <body>
            <h1>Headlines </h1>
            <b>{0}</b> </ br>
            <i>{1}</i> </ br>
            <p>{2}</p> </ br>
        </body>
    </html>""".format(first_article.get("title"), first_article.get("published"),
                      first_article.get("summary"))




if __name__ == '__main__':
    app.run(port=5000, debug=True)


#1) We need the base URL to activate the get_news() function

#2) In the argument the string in <> will create a variable with this name.
#   So we can call the base URL plus a argument to receive a specific
#   RSS-FEED.
#   @app.route("/<publication>") creates the variable "publication"
#   e.g. URL: localhost:5000/cnn --> result: publication = cnn
#   def get_news(publication=cnn)
#   feed = feedparser.parse(RSS_FEEDS[cnn]


# Any dynamic part of the route must contain a parameter of the same name
# in the function in order to use the value.
# e.g. @app.route("/<publication>") --> def get_news(publication)

