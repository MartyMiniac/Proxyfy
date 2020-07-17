from flask import Flask
from requests import get

app = Flask(__name__)
SITE_NAME = 'https://google.com/'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
  return get(path).content

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)