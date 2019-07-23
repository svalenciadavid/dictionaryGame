import os
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from data_classes import *
#import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class addUser():
    def post():
        new_user_data = User_data(parent=root_parent())
        new_user_data.user = users.get_current_user()
        new_user_data.name = users.get_current_user().email()
        new_user.wins = 0
        new_user.put()


def check_in_Database(current_user):
    user = User_data.query(User_data.user == current_user, ancestor=root_parent()).fetch()
    if not user:
        new_user_data = User_data(parent=root_parent())
        new_user_data.user = users.get_current_user()
        new_user_data.name = users.get_current_user().email()
        new_user_data.wins = 0
        new_user_data.put()


class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            check_in_Database(user)
            template = JINJA_ENVIRONMENT.get_template('templates/homePage/homePage.html')
        elif not user:
            template = JINJA_ENVIRONMENT.get_template('templates/loginPage/login.html')
        data = {
          'user': user,
          'login_url': users.create_login_url(self.request.uri),
          'logout_url': users.create_logout_url(self.request.uri),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

    def post(self):
        pass


# class PlayerPage(webapp2.RequestHandler):
#     def get(self):
#         template = JINJA_ENVIRONMENT.get_template('templates/homePage/homePage.html')
#         self.response.headers['Content-Type'] = 'text/html'
#         self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    #('/addUser',addUser),
    #('/host', HostPage),
    #('/player', PlayerPage)
], debug=True)
