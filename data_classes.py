from google.appengine.ext import ndb

def root_parent():
    return ndb.Key('Parent', 'default_parent')

class User_data(ndb.Model):
    name = ndb.StringProperty()
    wins = ndb.StringProperty()

class Game_state(ndb.Model):
    word = ndb.StringProperty()
    definition = ndb.StringProperty()

class Players(ndb.Model):
    name = ndb.StringProperty()
    score = ndb.IntegerProperty()
