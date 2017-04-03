import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class LaLigaSpider(CrawlSpider):
	name = "la_liga"
	start_urls = [
		'http://www.laliga.es/laliga-santander',
	]
	allowed_domains = ['www.laliga.es']
	rules = (
		Rule(LinkExtractor(allow=('^http\:\/\/www\.laliga\.es\/laliga-santander\/(.+)$',)), callback='parse_team', follow=True),
		Rule(LinkExtractor(allow=('^http\:\/\/www\.laliga\.es\/jugador\/(.+)$',)), callback='parse_player'),
	)
	
	def __init__(self, *a, **kw):
		super(LaLigaSpider, self).__init__(*a, **kw)

	def parse_team(self, response):
		team = response.css('#box-equipo .titulo::text').extract_first()
		if team is not None:
			yield {
				'type': 'team',
				'name': team
			}
		
	def parse_player(self, response):
		team = response.css('.cabecera-seccion .titulo::text').extract_first()
		yield {
			'type': 'player',
			'team': team,
			'nickname': response.css('#nickname::text').extract_first()
		}
		