import os

from google.appengine.ext import ndb

import jinja2
import webapp2

from google.appengine.api import users


def root_parent():
    return ndb.Key('Parent', 'default_parent')

class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/loginPage/login.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/home'),
          'logout_url': users.create_logout_url('/'),
        }
        template = JINJA_ENVIRONMENT.get_template('templates/loginPage/login.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

class HomePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/homePage/homePage.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/home'),
          'logout_url': users.create_logout_url('/'),
        }
        template = JINJA_ENVIRONMENT.get_template('templates/homePage/homePage.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/home', HomePage),
    #('/host', HostPage),
    #('/player', PlayerPage)
], debug=True)
