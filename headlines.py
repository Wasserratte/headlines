# Render_template with GET-Request
# https://github.com/Wasserratte/headlines.git
# Headlines

import feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest',
            'iol': 'http://www.iol.co.za/cmlink/1.640'}         

@app.route("/")         
    
def get_news(publication="bbc"):      

    query = request.args.get("publication")     #1

    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:                                           #2
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html",
                           articles=feed['entries'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)



#1) The user GET argument is automatically availabe in request.args.
#   In the home.html we define a variable with the name "publication" for
#   the searchbox. The request.args.get(publication) receives the value
#   that the user type into the searchbox e.g. bbc, cnn
#   It is important that the home.html and the Python request.args.get()
#   uses the same variable name.

#2) Check if it has the publication value(key for the RSS_FEEDS Dictionary) set
#   using the .get(). Return None if the key doesn't exist. If the correct
#   argument is there return the matching publication e.g. bbc, cnn

