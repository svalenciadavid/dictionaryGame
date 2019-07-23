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

#TEST
class AddGameState(webapp2.RequestHandler):
    def post(self):
        new_game_state = Game_state(parent=root_parent())
        new_game_state.word = "foo"
        new_game_state.definition = "a fooer"
        new_game_state.fake_definition = ""
        self.redirect("/host"+"?gameID="+new_game_state.put().urlsafe())


def add_to_Database(current_user):
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
        data = {
            'user': user,
            'login_url': users.create_login_url(self.request.uri),
            'logout_url': users.create_logout_url(self.request.uri),
        }
        if user:
            add_to_Database(user)
            data['user_data'] = User_data.query(User_data.user == user, ancestor=root_parent()).fetch()[0]
            template = JINJA_ENVIRONMENT.get_template('templates/homePage/homePage.html')
        elif not user:
            template = JINJA_ENVIRONMENT.get_template('templates/loginPage/login.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))
        word_json = getRandomWords()
        while "results" not in word_json or "definition" not in word_json["results"][0]:
            word_json = getRandomWords()

        print word_json


# API stuff- Fantah put under game page handler
def getRandomWords():
    headers = {"X-Mashape-Key": api_key.rapidapi_key,
        "Accept": "application/json"}
    result = urlfetch.fetch(
        url = "https://wordsapiv1.p.rapidapi.com/words/?random=true" ,
        # url='https://wordsapiv1.p.rapidapi.com/words/?random=true',
        headers=headers).content
    randomwords_json = json.loads(result)
    return randomwords_json



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

# class PlayerPage(webapp2.RequestHandler):
#     def get(self):
#         template = JINJA_ENVIRONMENT.get_template('templates/homePage/homePage.html')
#         self.response.headers['Content-Type'] = 'text/html'
#         self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/host', HostPage),
    ('/player', PlayerPage),
    ('/newgamestate', AddGameState)
], debug=True)
