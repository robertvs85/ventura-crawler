from dummy_crawler import crawler

crawler("http://www.laliga.es/", "^http\:\/\/www\.laliga\.es\/jugador\/(.+)$", "Iniesta", 1000)
