
import json
from scrapy.exceptions import DropItem
import pymongo

class PlayerPipeline(object):
	def open_spider(self, spider):
		self.file = open('players.jl', 'wb')

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		if item is not None and item['type'] == 'player':
			line = json.dumps(dict(item)) + "\n"
			self.file.write(line)
		return item

class TeamPipeline(object):
	def open_spider(self, spider):
		self.file = open('teams.jl', 'wb')

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		if item is not None and item['type'] == 'team':
			line = json.dumps(dict(item)) + "\n"
			self.file.write(line)
		return item

