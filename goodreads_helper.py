import requests
from requests_oauthlib import OAuth1Session
from flask import Flask, render_template, request, redirect, url_for

class GoodreadsHelper:

  REQUEST_TOKEN_URL = 'http://www.goodreads.com/oauth/request_token'
  BASE_AUTHORIZATION_URL = 'http://www.goodreads.com/oauth/authorize'
  ACCESS_TOKEN_URL='http://www.goodreads.com/oauth/access_token'

  def __init__(self):
    self.authorized = False

  def authorize(self, client_key, client_secret):
    self.client_key, self.client_secret = client_key, client_secret
    self.oauth = OAuth1Session(self.client_key,
        client_secret=self.client_secret)
    fetch_response = self.oauth.fetch_request_token(GoodreadsHelper.REQUEST_TOKEN_URL)
    self.resource_owner_key = fetch_response.get('oauth_token')
    self.resource_owner_secret = fetch_response.get('oauth_token_secret')
    authorization_url = self.oauth.authorization_url(GoodreadsHelper.BASE_AUTHORIZATION_URL)
    return redirect(authorization_url)  # redirects to /oauth-callback

  def handle_callback(self, redirect_response):
    oauth_response = self.oauth.parse_authorization_response(redirect_response)
    verifier = oauth_response.get('oauth_token')
    self.oauth = OAuth1Session(self.client_key, client_secret=self.client_secret,
        resource_owner_key=self.resource_owner_key,
        resource_owner_secret=self.resource_owner_secret,
        verifier=verifier)
    return self.__get_access_token()

  def __get_access_token(self):
    oauth_tokens = self.oauth.fetch_access_token(GoodreadsHelper.ACCESS_TOKEN_URL)
    self.resource_owner_key = oauth_tokens.get('oauth_token')
    self.resource_owner_secret = oauth_tokens.get('oauth_token_secret')
    self.oauth = OAuth1Session(self.client_key, client_secret=self.client_secret,
        resource_owner_key=self.resource_owner_key,
        resource_owner_secret=self.resource_owner_secret)
    self.authorized = True
    return redirect('/') # probably wont work

  # # returns books as
  # def get_books(self):
  #   if self.authorized:
  #     books_xml = self.__get_books_from_goodreads()
  #     books = self.__objectify_xml(books_xml)
  #     return books
  #   return []
  #
  # def __get_books_from_goodreads(self):
  #   request = requests.get()
  #   return
  #
  # def __get_uid_from_goodreads(self):
  #   response = requests.get('https://www.goodreads.com/api/auth_user')
  #   return request.data
  #
  # def __get_uid_from_xml(self, xml):
  #   return
  #
  # def __objectify_books_xml(self, books_xml):
  #   return
