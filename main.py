import os

from google.appengine.ext import ndb

import jinja2
import webapp2

from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/loginPage/login.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

app = webapp2.WSGIApplication([
    ('/', MainPage)
    #('/login', LoginPage),
    #('/home', HomePage),
    #('/host', HostPage),
    #('/player', PlayerPage)
], debug=True)
