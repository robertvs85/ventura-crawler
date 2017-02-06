from dummy_crawler import crawler, crawler2

crawler2("http://www.laliga.es/", "^http\:\/\/www\.laliga\.es\/jugador\/(.+)$", 1000)
#crawler("http://www.laliga.es/", "^http\:\/\/www\.laliga\.es\/jugador\/(.+)$", "Iniesta", 1000)
