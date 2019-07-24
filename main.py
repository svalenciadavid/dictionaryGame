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
        while ((("results" not in randomwords_json or "definition" not in randomwords_json["results"][0] and " " in randomwords_json["word"]))or ( " " in randomwords_json["word"])):
            randomwords_json= getRandomWords()
        data = {
            'user': user,
            'login_url': users.create_login_url(self.request.uri),
            'logout_url': users.create_logout_url(self.request.uri),
            'words': randomwords_json,
            'error' : ""
        }
        if user:
            add_to_Database(user)
            data['user_data'] = User_data.query(User_data.user == user, ancestor=root_parent()).fetch()[0]
            data['error'] = self.request.get('error')
            template = JINJA_ENVIRONMENT.get_template('templates/homePage/homePage.html')
        elif not user:
            template = JINJA_ENVIRONMENT.get_template('templates/loginPage/login.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))


# API stuff- Fantah put under game page handler



    #self.response.write(result.content) when responding to client
def link_player_game(current_user,gameID,isMaster = False):
    #We assume that the player is logged in and search for the user in the user_data data table,
    #This will allow us to acess that player's name
    player = User_data.query(User_data.user == current_user, ancestor=root_parent()).fetch()[0]
    new_player = Players(parent=root_parent())
    new_player.name = player.name
    new_player.email = player.user.email()
    # ndb.Key(urlsafe = gameID) Used to create a game key based on the
    new_player.gameKey = ndb.Key(urlsafe = gameID)
    new_player.isMaster = isMaster
    new_player.put()

class AddGameState(webapp2.RequestHandler):
    def post(self):
        # New Game State Created
        new_game_state = Game_state(parent=root_parent())
        new_game_state.word = "foo"
        new_game_state.definition = "a fooer"
        new_game_state.fake_definition = ""
        gameKey = new_game_state.put()
        link_player_game(users.get_current_user(), gameKey.urlsafe(), isMaster = True)
        self.redirect("/player?gameID="+gameKey.urlsafe())
        # Link Player to the game # ID
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
        # We try to get the game key by looking at the urlsafe in the search bar
        try:
            url = self.request.get('gameID')
            gameKey = ndb.Key(urlsafe = url)
        except:
            # The redirect doesn't end the function so return will
            self.redirect('/?error="That is not a valid Key!!"')
            return
        try:
            #Then we try to get the current logged in player by their current game and through their email as their identifier
            currentPlayer = Players.query(Players.gameKey == gameKey and Players.email == users.get_current_user().email(),  ancestor=root_parent()).fetch()[0]
        except:
            #If it doesn't exist then we assume this is a new player going in the game
            #So we will add them to the database   isMaster = False by default
            link_player_game(users.get_current_user(), url)
            #Now we try to get the Player again-- let's assume this works since we just added them above
            currentPlayer = Players.query(Players.gameKey == gameKey and Players.email == users.get_current_user().email(),  ancestor=root_parent()).fetch()[0]

        # Now let's Dance!

        #get all players from the game by their game key -> LeaderBoard Purposes
        players = Players.query( Players.gameKey ==  gameKey,ancestor=root_parent())
        # We update our data dictionary with these values
        data = {
        "players" : players,
        "currentPlayer" : currentPlayer
        }
        
        # Now it's time to determine this player's role to display the correct html page
        if currentPlayer.isMaster == True:
            template = JINJA_ENVIRONMENT.get_template('templates/gamePage/hostPage.html')
        elif currentPlayer.isMaster == False:
            template = JINJA_ENVIRONMENT.get_template('templates/gamePage/regularPlayer.html')
        # Finally we render the HTML page
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    #('/host', HostPage),
    ('/player', PlayerPage),
    ('/newgamestate', AddGameState)
], debug=True)
