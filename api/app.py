import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.escape
import motor
import json
from tornado.gen import coroutine
from react.render import render_component
import os

class TeamsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, PATCH, DELETE")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
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
        
    def options(self):
        # no body
        self.set_status(204)
        self.finish()
        
 
class AllPlayersHandler(tornado.web.RequestHandler):
   
    def initialize(self, mongo_db):
       self.mongo_db = mongo_db
    
    @tornado.gen.coroutine
    def get(self):
        sort_by = self.get_argument('sort_by', 'number')
        cursor = mongo_db.players.find({},{'_id': 0}).sort([(sort_by, 1)])
        players = []
        while (yield cursor.fetch_next):
            document = cursor.next_object()
            players.append(document)
        result = {
            'players': players
        }
        self.write(result)

class PlayersHandler(tornado.web.RequestHandler):
   
    def initialize(self, mongo_db):
       self.mongo_db = mongo_db
    
    @tornado.gen.coroutine
    def get(self, team, field):
        self.field_to_show = field
        sort_by = self.get_argument('sort_by', 'number')
        cursor = mongo_db.players.find({'team':team},{'_id': 0}).sort([(sort_by, 1)])
        players = []
        while (yield cursor.fetch_next):
            document = cursor.next_object()
            players.append(document[field] if len(field) > 0 else document)
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
        
class IndexHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        rendered = render_component(
        os.path.join(os.getcwd(), 'webapp', 'laliga.jsx'),
        {},
        to_static_markup=False,
        )
        self.render('webapp/index.html', rendered=rendered)

def make_app(mongo_db):
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/teams", TeamsHandler, dict(mongo_db=mongo_db)),
        (r"/players", AllPlayersHandler, dict(mongo_db=mongo_db)),
        (r"/players/(.*)/(.*)", PlayersHandler, dict(mongo_db=mongo_db)),
        (r"/player/(.*)", SinglePlayerHandler, dict(mongo_db=mongo_db))
    ])

if __name__ == "__main__":
    mongo_con = motor.motor_tornado.MotorClient('mongodb://admin:ventura2017@ds145780.mlab.com:45780/soccer_stats')
    mongo_db = mongo_con.soccer_stats
    app = make_app(mongo_db)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()