from flask import *
from requests import get
from bs4 import *

app = Flask(__name__)
SITE_NAME = 'https://google.com/'

@app.route('/')
def index():
  return "please enter the url after / or use /go/<url> for experimental version"

@app.route('/<path:path>')
def proxy(path):
  if path[:8] !='https://':
    path='https://'+path

  html=get(path).text

  soup = BeautifulSoup(html, 'html.parser')
  for allLinks in soup.find_all(href=True):
    if allLinks['href'] and not allLinks['href'].startswith("http"):
      if allLinks['href'][:2]=='//':
        allLinks['href']='/https:'+allLinks['href']
        continue
      allLinks['href']='/'+path+allLinks['href']

  for allLinks in soup.find_all(src=True):
      if allLinks['src'] and not allLinks['src'].startswith("http"):
        if allLinks['src'][:2]=='//':
          continue
        allLinks['src']=path[:-1]+allLinks['src']

  for allLinks in soup.find_all('form'):
    allLinks['action']='/'+path+allLinks['action']


  #return get(path).content
  #return render_template('test.html')
  return soup.prettify('utf-8')

@app.route('/go/<path:path>')
def goproxy(path):
  if path[:8] !='https://':
    path='https://'+path

  return get(path).content

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
