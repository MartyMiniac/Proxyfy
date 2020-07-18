from flask import *
from requests import get
from bs4 import *

app = Flask(__name__)
SITE_NAME = 'https://google.com/'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
  if path[:8] !='https://':
    path='https://'+path

  html=get(path).text

  soup = BeautifulSoup(html, 'html.parser')
  for i in soup.find_all('img'):
    url=i.get('src')
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


  #return get(path).content
  #return render_template('test.html')
  return soup.prettify('utf-8')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)