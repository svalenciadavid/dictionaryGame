import os
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import data_classes
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        print user
        if user:
            print "SEEEE"
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
        word_json = getRandomWords()
        while "results" not in word_json or "definition" not in word_json["results"][0]:
            word_json = getRandomWords()

        print word_json


# API stuff- Fantah put under game page handler
def getRandomWords():
    headers = {"X-Mashape-Key": "9a227e9a3fmshf2acd8cd4c36bdep171891jsn85aad3ecccee",
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
    #('/main', MainPage),
    ('/host', HostPage),
    ('/player', PlayerPage)
], debug=True)
