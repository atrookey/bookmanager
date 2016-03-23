from flask import Flask, render_template, request, redirect, url_for
import goodreads_helper

app = Flask(__name__)
app.config.from_envvar('BOOK_MANAGER_SETTINGS')

goodreads = goodreads_helper.GoodreadsHelper()

@app.route('/')
def home():
  if not goodreads.authorized:
    client_key = app.config['GOODREADS_PUBLIC_KEY']
    client_secret = app.config['GOODREADS_SECRET_KEY']
    return goodreads.authorize(client_key, client_secret)
  return render_template('pages/home.html')

# TODO (atrookey) change to /oauth-callback
@app.route('/authorization_redirect')
def authorization_redirect():
  redirect_response = request.url
  return goodreads.handle_callback(redirect_response)

@app.errorhandler(404)
def not_found_error(error):
  return render_template('errors/404.html'), 404

if not app.debug:
  file_handler = FileHandler('error.log')
  file_handler.setFormatter(
      Formatter('%(asctime)s %(levelname)s: %(message)s '
          '[in %(pathname)s:%(lineno)d]')
  )
  app.logger.setLevel(logging.INFO)
  file_handler.setLevel(logging.INFO)
  app.logger.addHandler(file_handler)
  app.logger.info('errors')

if __name__ == '__main__':
  app.run(host='0.0.0.0')
