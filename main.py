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


def add_to_Database(current_user):
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
        randomwords_json = getRandomWords()
        while ((("results" not in randomwords_json or "definition" not in randomwords_json["results"][0] and "" in randomwords_json["word"]))or ( " " in randomwords_json["word"])):
            randomwords_json= getRandomWords()
        data = {
            'user': user,
            'login_url': users.create_login_url(self.request.uri),
            'logout_url': users.create_logout_url(self.request.uri),
            'words': randomwords_json,
        }
        if user:
            add_to_Database(user)
            data['user_data'] = User_data.query(User_data.user == user, ancestor=root_parent()).fetch()[0]
            template = JINJA_ENVIRONMENT.get_template('templates/homePage/homePage.html')
        elif not user:
            template = JINJA_ENVIRONMENT.get_template('templates/loginPage/login.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))


# API stuff- Fantah put under game page handler



    #self.response.write(result.content) when responding to client

class AddGameState(webapp2.RequestHandler):
    def post(self):
        # New Game State Created
        new_game_state = Game_state(parent=root_parent())
        new_game_state.word = "foo"
        new_game_state.definition = "a fooer"
        new_game_state.fake_definition = ""
        gameKey = new_game_state.put()
        link_player_game(users.get_current_user(), gameKey.urlsafe(), isMaster = True)
        self.redirect("/player"+"?gameID="+gameKey.urlsafe())
        # Link Player to the game # ID
def link_player_game(current_user,gameID,isMaster = False):
    #We assume that the player is logged in and search for the user in the user_data data table,
    #This will allow us to acess that player's name
    player = User_data.query(User_data.user == current_user, ancestor=root_parent()).fetch()[0]
    new_player = Players(parent=root_parent())
    new_player.name = player.name
    new_player.email = player.user.email()
    new_player.gameKey = ndb.Key(urlsafe = gameID)
    new_player.isMaster = isMaster
    new_player.put()
# class HostPage(webapp2.RequestHandler):
#     def get(self):
#         self.request.get("gameID")
#         template = JINJA_ENVIRONMENT.get_template('templates/gamePage/hostPage.html')
#         self.response.headers['Content-Type'] = 'text/html'
#         self.response.write(template.render())
#
# class PlayerPage(webapp2.RequestHandler):
#     def get(self):
#         template = JINJA_ENVIRONMENT.get_template('templates/gamePage/regularPlayer.html')
#         self.response.headers['Content-Type'] = 'text/html'
#         self.response.write(template.render())

class PlayerPage(webapp2.RequestHandler):
    def get(self):
        currentPlayer = Players.query(Players.email == users.get_current_user().email()).fetch()
        data = {
        "players" : Players.query().fetch()[0]
        }
        template = JINJA_ENVIRONMENT.get_template('templates/gamePage/hostPage.html')
        #template = JINJA_ENVIRONMENT.get_template('templates/gamePage/regularPlayer.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    #('/host', HostPage),
    ('/player', PlayerPage),
    ('/newgamestate', AddGameState)
], debug=True)
