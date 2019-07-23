import os
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from data_classes import *
#import json
from google.appengine.api import urlfetch
import json
import api_key

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

def getRandomWords():
    headers = {"X-Mashape-Key": api_key.rapidapi_key,
        "Accept": "application/json"}
    result = urlfetch.fetch(
        url = "https://wordsapiv1.p.rapidapi.com/words/?random=true" ,
        # url='https://wordsapiv1.p.rapidapi.com/words/?random=true',
        headers=headers).content
    randomwords_json = json.loads(result)
    return randomwords_json


class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        data = {
            'user': user,
            'login_url': users.create_login_url(self.request.uri),
            'logout_url': users.create_logout_url(self.request.uri),
        }
        if user:
            check_in_Database(user)
            data['user_data'] = User_data.query(User_data.user == user, ancestor=root_parent()).fetch()[0]
            template = JINJA_ENVIRONMENT.get_template('templates/homePage/homePage.html')
        elif not user:
            template = JINJA_ENVIRONMENT.get_template('templates/loginPage/login.html')
        self.response.headers['Content-Type'] = 'text/html'
        # self.response.write(template.render(data))
        index_template = JINJA_ENVIRONMENT.get_template('templates/loginPage/login.html')
        randomwords_json = getRandomWords()
        while ("results" not in randomwords_json or "definition" not in randomwords_json["results"][0]):
            randomwords_json= getRandomWords()
        values = {
            'words': randomwords_json,
            }
        self.response.write(index_template.render(values))
        # while "results" not in word_json or "definition" not in word_json["results"][0]:
        #     word_json = getRandomWords()
        #
        # print word_json


# API stuff- Fantah put under game page handler



    #self.response.write(result.content) when responding to client


class HostPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/gamePage/hostPage.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())

class PlayerPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/gamePage/regularPlayer.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())


    def post(self):
        pass


# class PlayerPage(webapp2.RequestHandler):
#     def get(self):
#         template = JINJA_ENVIRONMENT.get_template('templates/homePage/homePage.html')
#         self.response.headers['Content-Type'] = 'text/html'
#         self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/host', HostPage),
    ('/player', PlayerPage),
], debug=True)
