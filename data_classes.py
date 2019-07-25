from google.appengine.ext import ndb

def root_parent():
    return ndb.Key('Parent', 'default_parent')

class User_data(ndb.Model):
    user = ndb.UserProperty()
    name = ndb.StringProperty()
    wins = ndb.IntegerProperty()

#games
class Game_state(ndb.Model):
    word = ndb.StringProperty()
    definition = ndb.StringProperty()
    fake_definition = ndb.StringProperty()

class Players(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    score = ndb.IntegerProperty(default = 0)
    isMaster = ndb.BooleanProperty()
    gameKey = ndb.KeyProperty()
    isDone = ndb.BooleanProperty(default = False)
