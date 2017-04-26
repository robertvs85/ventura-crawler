
import json
from scrapy.exceptions import DropItem
import pymongo

class PlayerPipeline(object):
	def open_spider(self, spider):
		self.file = open('players.jl', 'w')

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		if item is not None and item['type'] == 'player':
			line = json.dumps(dict(item)) + "\n"
			self.file.write(line)
		return item

class TeamPipeline(object):
	def open_spider(self, spider):
		self.file = open('teams.jl', 'w')

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		if item is not None and item['type'] == 'team':
			line = json.dumps(dict(item)) + "\n"
			self.file.write(line)
		return item

class PlayerMongoPipeline(object):

	collection_name = 'players'

	def __init__(self, mongo_uri, mongo_db):
		self.mongo_uri = mongo_uri
		self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			mongo_uri=crawler.settings.get('MONGO_URI'),
			mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
		)

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]
 
	def close_spider(self, spider):
		self.client.close()

	def process_item(self, item, spider):
		if item is not None and item['type'] == 'player':
			self.db[self.collection_name].update_one({'nickname': item['nickname']}, {'$set': dict(item)}, upsert=True)
		return item
		
class TeamMongoPipeline(object):

	collection_name = 'teams'

	def __init__(self, mongo_uri, mongo_db):
		self.mongo_uri = mongo_uri
		self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			mongo_uri=crawler.settings.get('MONGO_URI'),
			mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
		)

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]

	def close_spider(self, spider):
		self.client.close()

	def process_item(self, item, spider):
		if item is not None and item['type'] == 'team':
			self.db[self.collection_name].update_one({'name': item['name']}, {'$set': dict(item)}, upsert=True)
		return item