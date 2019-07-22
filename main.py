import os

from google.appenginge.ext import nbd

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', DogPage),
    ('/home', CatPage),
    ('/host', DeleteDogs),
    ('/player', DeleteCats)
], debug=True)
