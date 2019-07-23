import os
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import data_classes

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





# class PlayerPage(webapp2.RequestHandler):
#     def get(self):
#         template = JINJA_ENVIRONMENT.get_template('templates/homePage/homePage.html')
#         self.response.headers['Content-Type'] = 'text/html'
#         self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    #('/main', MainPage),
    #('/host', HostPage),
    #('/player', PlayerPage)
], debug=True)
