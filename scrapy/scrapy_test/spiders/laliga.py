#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
	personal_stats_mapping = {
		'Fecha nacimiento': 'birth_date',
		'Lugar de nacimiento': 'city_birth',
		'Altura': 'height',
		'Peso': 'weight',
		'Nacionalidad': 'nationality',
		u'Posici\xf3n': 'position'
	}
	
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
		profile = response.css('#datos-perfil')
		personal_stats = response.css('#ficha-jugador .datos-sidebar-jugador .box-datos .box-dato')
		football_stats = response.css('#estadisticas-1')
		
		player_data = {
			'type': 'player',
			'team': team,
			'nickname': profile.css('#nickname::text').extract_first(),
			'full_name': profile.css('#nombre::text').extract_first(),
			'number': profile.css('#dorsal::text').extract_first(),
			'personal_stats': {
				
			},
			'football_stats': {
				'recoveries': football_stats.css('#estadisticas-defensa .valor::text').extract_first(),
				'passes': football_stats.css('#estadisticas-contruccion .valor::text').extract_first(),
				'shots': football_stats.css('#estadisticas-ataque .valor::text').extract_first(),
				'goals': football_stats.css('#estadisticas-goles .valor::text').extract_first(),
				'yellow_cards': football_stats.css('#estadisticas-disciplina .tarjetas-amarillas .valor::text').extract_first(),
				'red_cards': football_stats.css('#estadisticas-disciplina .tarjetas-rojas .valor::text').extract_first(),
				'minutes': response.css('#datos-jugador-der .destacado::text').extract_first()
			} 
		}
		
		for value in personal_stats:
			header = value.css('h2::text').extract_first()
			key = self.personal_stats_mapping.get(header, None)
			if key is not None:
				player_data['personal_stats'][key] = value.css('.dato::text').extract_first()
		
		yield player_data
		
		