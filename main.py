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
        #Randomizing/getting words
        randomwords_json = getRandomWords()
        while ((("results" not in randomwords_json or "definition" not in randomwords_json["results"][0] and " " in randomwords_json["word"]))or ( " " in randomwords_json["word"])):
            randomwords_json= getRandomWords()
        generated_word = randomwords_json["word"]

        generated_def = randomwords_json["results"][0]["definition"]

        #Instantiating state
        new_game_state = Game_state(parent=root_parent())
        new_game_state.word = generated_word
        new_game_state.definition = generated_def
        new_game_state.fake_definition = ""
        gameKey = new_game_state.put()
        link_player_game(users.get_current_user(), gameKey.urlsafe(), isMaster = True)
        self.redirect("/player?gameID="+gameKey.urlsafe())

class updateGameState(webapp2.RequestHandler):
    def get(self):
        pass
    def post(self):
        url = self.request.get('gameID')
        gameKey = ndb.Key(urlsafe = url)
        currentGame = gameKey.get()
        #UPDATE THE CURRENT Game
        randomwords_json = getRandomWords()
        while ((("results" not in randomwords_json or "definition" not in randomwords_json["results"][0] and " " in randomwords_json["word"]))or ( " " in randomwords_json["word"])):
            randomwords_json= getRandomWords()
        generated_word = randomwords_json["word"]

        generated_def = randomwords_json["results"][0]["definition"]
        currentGame.word = generated_word
        currentGame.definition = generated_def
        currentGame.fake_definition = ""
        currentGame.put()
        ###players
        #We gotta make all the players notDone again!!
        # for player in players:
        #     player.isDone = False
        #     player.put()

        self.redirect('/player?gameID='+url)

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
class ajax_refresh(webapp2.RequestHandler):
    def get(self):
        print("RRUUUUUUUUUUUUUUUUUUUUUUUUUUUNGKLNDSLFsdfN/n/n/n/n/n\n\n\n\n\n\n\n")
        url = self.request.get('gameID')
        gameKey = ndb.Key(urlsafe = url)
        print("RROOOOOOOOOOOOOOOOOOOOOOOOOOON")
        # Now let's Dance!
        #get all players from the game by their game key -> LeaderBoard Purposes
        players = Players.query( Players.gameKey ==  gameKey,ancestor=root_parent()).fetch()
        currentGame = gameKey.get()
        willRedirect = True
        for player in players:
            if player.isDone:
                pass
            elif player.isDone == False:
                willRedirect = False
        retDict = {
        "willRedirect" : willRedirect
        }
        self.response.headers['Content-Type'] = 'application/json'
        # Turn data dict into a json string and write it to the response
        self.response.write(json.dumps(retDict))
        #self.response.write()
        # self.redirect('/player?gameID='+url)



class get_current_definiton(webapp2.RequestHandler):
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
            currentPlayer = Players.query(Players.gameKey == gameKey, Players.email == users.get_current_user().email(),  ancestor=root_parent()).fetch()[0]
        except:
            #If it doesn't exist then we assume this is a new player going in the game
            #So we will add them to the database   isMaster = False by default
            link_player_game(users.get_current_user(), url)
            #Now we try to get the Player again-- let's assume this works since we just added them above
            currentPlayer = Players.query(Players.gameKey == gameKey, Players.email == users.get_current_user().email(),  ancestor=root_parent()).fetch()[0]

        # Now let's Dance!

        #get all players from the game by their game key -> LeaderBoard Purposes
        players = Players.query( Players.gameKey ==  gameKey,ancestor=root_parent()).fetch()
        currentGame = gameKey.get()
        user = users.get_current_user()

        if user is None:
            # No user is logged in, so don't return any value.
            self.response.status = 401
            return
        user_definition = currentGame.fake_definition
        user_word = currentGame.word
        # build a dictionary that contains the data that we want to return.
        data = {'fake_definition': user_definition,
                'word' : user_word }
        # Note the different content type.
        self.response.headers['Content-Type'] = 'application/json'
        # Turn data dict into a json string and write it to the response
        self.response.write(json.dumps(data))


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
            currentPlayer = Players.query(Players.gameKey == gameKey, Players.email == users.get_current_user().email(),  ancestor=root_parent()).fetch()[0]
        except:
            #If it doesn't exist then we assume this is a new player going in the game
            #So we will add them to the database   isMaster = False by default
            link_player_game(users.get_current_user(), url)
            #Now we try to get the Player again-- let's assume this works since we just added them above
            currentPlayer = Players.query(Players.gameKey == gameKey, Players.email == users.get_current_user().email(),  ancestor=root_parent()).fetch()[0]

        # Now let's Dance!

        #get all players from the game by their game key -> LeaderBoard Purposes
        players = Players.query( Players.gameKey ==  gameKey,ancestor=root_parent()).fetch()
        currentGame = gameKey.get()
        # We update our data dictionary with these values
        #currentGame = Game_state.query( Game_state.id == gameKey,ancestor=root_parent()).fetch()[0]
        data = {
        "players" : players,
        "currentPlayer" : currentPlayer,
        "word" : currentGame.word,
        "url" : url
        }
                # Now it's time to determine this player's role to display the correct html page
        if currentPlayer.isMaster == True:
            data["definition"]= currentGame.definition
            data["fake_definition"]= currentGame.fake_definition
            template = JINJA_ENVIRONMENT.get_template('templates/gamePage/hostPage.html')
        elif currentPlayer.isMaster == False:
            data["fake_definition"]= currentGame.fake_definition
            template = JINJA_ENVIRONMENT.get_template('templates/gamePage/regularPlayer.html')
        # Finally we render the HTML page
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))
    def post(self):
        ## Getting key and current player
        url = self.request.get('gameID')
        gameKey = ndb.Key(urlsafe = url)
        players = Players.query( Players.gameKey ==  gameKey,ancestor=root_parent()).fetch()
        currentPlayer = Players.query(Players.gameKey == gameKey, Players.email == users.get_current_user().email(),  ancestor=root_parent()).fetch()[0]
        currentGame = gameKey.get()
        if currentPlayer.isMaster == True:
            currentGame.fake_definition = self.request.get("fakeDefinition")
            currentGame.put()
            currentPlayer.isDone = True
            currentPlayer.put()
            #self.redirect('/standBy?gameID='+url)
            self.redirect('/standBy?gameID='+url)
        elif currentPlayer.isMaster == False:
            #We try to get the answer to the # QUESTION:
            answer = self.request.get("check")
            if currentPlayer.isDone == False:
                if answer == "real":
                    if currentGame.definition == currentGame.fake_definition:
                        currentPlayer.score = currentPlayer.score+1
                    else:
                        for player in players:
                            if player.isMaster:
                                player.score = player.score+1
                                player.put()
                elif answer == "fake":
                    if currentGame.definition == currentGame.fake_definition:
                        for player in players:
                            if player.isMaster:
                                player.score = player.score+1
                                player.put()
                    else:
                        currentPlayer.score = currentPlayer.score+1

            currentPlayer.isDone = True
            currentPlayer.put()
            self.redirect('/player?gameID='+url)

class standByPage(webapp2.RequestHandler):
    def get(self):
        url = self.request.get('gameID')
        gameKey = ndb.Key(urlsafe = url)
        currentPlayer = Players.query(Players.gameKey == gameKey, Players.email == users.get_current_user().email(),  ancestor=root_parent()).fetch()[0]

        print self.request.get("fakeDefinition")
        template = JINJA_ENVIRONMENT.get_template('templates/gamePage/standBy.html')
        data = {
        "currentPlayer" : currentPlayer

        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))
        #self.redirect('/player?gameID='+url)
    def post(self):
        pass

class LearnMore(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/loginPage/learnMore.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/player', PlayerPage),
    ('/newgamestate', AddGameState),
    ('/standBy', standByPage),
    ('/ajax/get_def', get_current_definiton),
    ('/ajax/refresh', ajax_refresh),
    ('/learnmore', LearnMore),
], debug=True)
