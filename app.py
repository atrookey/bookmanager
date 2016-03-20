import requests
from requests_oauthlib import OAuth1Session
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config.from_envvar('BOOK_MANAGER_SETTINGS')

not_authorized = True
request_token_url = 'http://www.goodreads.com/oauth/request_token'
base_authorization_url = 'http://www.goodreads.com/oauth/authorize'
access_token_url='http://www.goodreads.com/oauth/access_token'
client_key = app.config['GOODREADS_PUBLIC_KEY']
client_secret = app.config['GOODREADS_SECRET_KEY']

def authorize_goodreads():
  obtain_request_token()
  return obtain_authorization()

def obtain_request_token():
  global oauth
  global resource_owner_key
  global resource_owner_secret
  oauth = OAuth1Session(client_key, client_secret=client_secret)
  fetch_response = oauth.fetch_request_token(request_token_url)
  resource_owner_key = fetch_response.get('oauth_token')
  resource_owner_secret = fetch_response.get('oauth_token_secret')

def obtain_authorization():
  authorization_url = oauth.authorization_url(base_authorization_url)
  return redirect(authorization_url)  # redirects to /authorization_redirect

def obtain_access_token():
  oauth = OAuth1Session(client_key, client_secret=client_secret,
      resource_owner_key=resource_owner_key,
      resource_owner_secret=resource_owner_secret,
      verifier=verifier)
  oauth_tokens = oauth.fetch_access_token(access_token_url)
  resource_owner_key = oauth_tokens.get('oauth_token')
  resource_owner_secret = oauth_tokens.get('oauth_token_secret')
  new_oauth_session(resource_owner_key, resource_owner_secret)

def new_oauth_session():
  oauth = OAuth1Session(client_key,
      client_secret=client_secret, resource_owner_key=resource_owner_key,
      resource_owner_secret=resource_owner_secret)
  return redirect(url_for('authorized_successfully'))



@app.route('/')
def home():
  if not_authorized:
    return authorize_goodreads()
  return render_template('pages/home.html')

@app.route('/authorization_redirect')
def authorization_redirect():
  print('you made it to the redirect!!')
  global verifier
  redirect_response = request.url
  print(redirect_response)
  oauth_response = oauth.parse_authorization_response(redirect_response)
  verifier = oauth_response.get('oauth_verifier')
  return new_oauth_session()

@app.route('/authorized_successfully')
def authorized_successfully():
  return 'Whooooooooooooooooooo'

@app.errorhandler(404)
def not_found_error(error):
  return render_template('errors/404.html'), 404

if not app.debug:
  file_handler = FileHandler('error.log')
  file_handler.setFormatter(
      Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
  )
  app.logger.setLevel(logging.INFO)
  file_handler.setLevel(logging.INFO)
  app.logger.addHandler(file_handler)
  app.logger.info('errors')

if __name__ == '__main__':
  app.run(host='0.0.0.0')
