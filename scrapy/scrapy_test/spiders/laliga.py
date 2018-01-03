#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class LaLigaSpider(CrawlSpider):
	name = "la_liga"
	start_urls = [
		'http://www.laliga.es/laliga-santander/barcelona',
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
	team_stats_mapping = {
		u'A\xf1o fundaci\xf3n': 'foundation_year',
		'Presidente': 'president',
		'E-mail': 'email',
		'Temporadas en LaLiga Santander': 'seasons_in_1st_division',
		'Temporadas en LaLiga 1|2|3': 'seasons_in_2nd_division',
		u'N\xfam de socios': 'number_of_members',
		u'N\xfam de abonados': 'number_of_subscribers',
		'Firma deportiva': 'sports_firm',
		'Estadio': 'stadium',
		'Dimensiones Estadio': 'stadium_dimensions',
		'Aforo': 'capacity'
	}
	
	def __init__(self, *a, **kw):
		super(LaLigaSpider, self).__init__(*a, **kw)

	def parse_team(self, response):
		team = response.css('#box-equipo .titulo::text').extract_first()
		
		team_stats = response.css('.box-datos-sidebar')
		
		team_data = {
			'type': 'team',
			'name': team,
			'team_stats': {
				
			}
		}
		
		nombre = None
		
		for stat in team_stats.css('.box-dato'):
			key = stat.css('.nombre::text').extract_first()
			value = stat.css('.dato::text').extract_first()
			team_data['team_stats'][key] = value
		
		if team is not None:
			yield team_data
		
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
			'number': int(profile.css('#dorsal::text').extract_first()) if profile.css('#dorsal::text').extract_first() is not None else None,
			'position': profile.css('#posicion::text').extract_first(),
			'birth_date': profile.css('#fecha_nacimiento::text').extract_first().replace('Fecha nacimiento: ','') if profile.css('#fecha_nacimiento::text').extract_first() is not None else None,
			'city': profile.css('#lugar_nacimiento::text').extract_first().replace('Lugar de nacimiento: ','') if profile.css('#lugar_nacimiento::text').extract_first() is not None else None,
			'nationality': profile.css('#nacionalidad::text').extract_first().replace('Nacionalidad: ','') if profile.css('#nacionalidad::text').extract_first() is not None else None,
			'football_stats': {} 
		}
		
		for stat in personal_stats.css('.box-dato'):
			key = stat.css('.nombre::text').extract_first()
			value = stat.css('.dato::text').extract_first()
			player_data[key] = value
		
		i = 0
		for stat in response.css('.estadisticas_jugador_tabla tr'):
			if i % 2 == 0:
				columns = []
			j = 0
			for col in stat.css('td .estadisticas_jugador_dato::text').extract():
				if i % 2 == 0:
					columns.append(col)
				else:
					player_data['football_stats'][columns[j]] = int(col) if col.isdigit() else col
				j += 1

			i += 1
		
		yield player_data
		
		