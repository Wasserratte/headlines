# Render_template
# https://github.com/Wasserratte/headlines.git
# Headlines

import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest',
            'iol': 'http://www.iol.co.za/cmlink/1.640'}         

@app.route("/")         
@app.route("/<publication>")    
def get_news(publication="bbc"):      
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html",
                           articles=feed['entries'])     #1 


if __name__ == '__main__':
    app.run(port=5000, debug=True)


#1) Puts the whole content of the Feedsite into the variable article
#   Jinja will looping through all the articles and displaying the information
#   we want


