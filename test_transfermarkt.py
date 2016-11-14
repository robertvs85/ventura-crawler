from dummy_crawler import crawler

crawler("http://www.transfermarkt.es/", "^http\:\/\/www\.transfermarkt\.es\/(.+)\/profil\/spieler\/(.+)$", "Iniesta", 1000)
