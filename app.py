import os
import requests
from lxml import html

from flask import request
from flask import Flask
from flask import Response


app = Flask(__name__)

headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
}

@app.route('/', defaults={'path': 'google.com'})
@app.route('/<path:path>')
def root(path):    
    url = 'https://' + path
    print('URL:', url)
    r = requests.get(url, verify=False, headers=headers)
    r.raise_for_status()
    rr = Response(response=r.content, status=r.status_code)
    rr.headers["Content-Type"] = r.headers['Content-Type']
    return rr

@app.route('/g/<keyword>')
def gkeyword(keyword):    
    url = 'https://www.google.com/search'
    payload = {'q':keyword, 'num':1, 'start':1, 'sourceid':'chrome', 'ie':'UTF-8', 'cr':'cr=countryUS'}
    r = requests.get(url, params=payload)
    rr = Response(response=r.content, status=r.status_code)
    rr.headers["Content-Type"] = r.headers['Content-Type']
    return rr

@app.route('/r/<subreddit>/subscribers')
def gsubreddit(subreddit):
    url = 'https://old.reddit.com/r/' + subreddit
    xpath ="//span[@class='subscribers']/span[@class='number']/text()"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    tree = html.fromstring(r.content)
    subscribers = tree.xpath(xpath)
    rr = Response(response=subscribers, status=r.status_code)
    rr.headers["Content-Type"] = r.headers['Content-Type']
    return rr

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
