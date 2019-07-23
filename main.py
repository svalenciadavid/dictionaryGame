import os
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import data_classes
#import json

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
#class HomePage(webapp2.RequestHandler):
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
#def get_random_words(num):
    #random_url = 'https://wordsapiv1.p.mashape.com/words?random=true'
    #random_resp = urlfetch.Fetch(random_url).content
    #return json.loads(random_resp)

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    #('/home', HomePage),
    #('/host', HostPage),
    #('/player', PlayerPage)
], debug=True)
