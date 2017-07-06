import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.escape
import motor
import json

class TeamsHandler(tornado.web.RequestHandler):
   
    def initialize(self, mongo_db):
       self.mongo_db = mongo_db
    
    @tornado.gen.coroutine
    def get(self):
        cursor = mongo_db.teams.find({},{'_id': 0})
        teams = []
        while (yield cursor.fetch_next):
            document = cursor.next_object()
            teams.append(document)
        result = {
            'teams': teams
        }
        self.write(result)
        
class PlayersHandler(tornado.web.RequestHandler):
   
    def initialize(self, mongo_db):
       self.mongo_db = mongo_db
    
    @tornado.gen.coroutine
    def get(self, team, field):
        self.field_to_show = field
        cursor = mongo_db.players.find({'team':team},{'_id': 0})
        players = []
        while (yield cursor.fetch_next):
            document = cursor.next_object()
            players.append(document[field])
        result = {
            'players': players
        }
        self.write(result)

class SinglePlayerHandler(tornado.web.RequestHandler):
   
    def initialize(self, mongo_db):
       self.mongo_db = mongo_db
    
    @tornado.gen.coroutine
    def get(self, player):
        document = yield mongo_db.players.find_one({'nickname':player},{'_id': 0})
        self.write(document)        
        
def make_app(mongo_db):
    return tornado.web.Application([
        (r"/teams", TeamsHandler, dict(mongo_db=mongo_db)),
        (r"/players/(.*)/(.*)", PlayersHandler, dict(mongo_db=mongo_db)),
        (r"/player/(.*)", SinglePlayerHandler, dict(mongo_db=mongo_db)),
    ])

if __name__ == "__main__":
    mongo_con = motor.motor_tornado.MotorClient('mongodb://admin:ventura2017@ds145780.mlab.com:45780/soccer_stats')
    mongo_db = mongo_con.soccer_stats
    app = make_app(mongo_db)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()