from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

# Reimplementing HTMLParser to handle tags
class LinkParser(HTMLParser):

	def handle_starttag(self, tag, attrs):
		# Handling anchors
		if tag == 'a':
			for (key, value) in attrs:
				if key == 'href':
					newUrl = parse.urljoin(self.baseUrl, value)
					# Add to new links if it hasn't been visited yet
					if newUrl.startswith("http") and newUrl not in self.visited_urls:
						self.links = self.links + [newUrl]

	# New function, doesn't exist in HTMLParser, allows to pass extra parameters
	def setValues(self, url, visited_urls):
		self.initial_link = url
		self.visited_urls = visited_urls
	
	# New function, allows to get new links, together with the HTML content of the current page
	def getLinks(self, url, visited_urls):
		self.setValues(url, visited_urls)
		self.links = []
		# Remember the base URL which will be important when creating absolute URLs
		self.baseUrl = url
		response = urlopen(url)
		# Make sure that we are looking at HTML and not other things, handling different content types
		if response.getheader('Content-Type') in ('text/html', 'text/html; charset=utf-8'):
			htmlBytes = response.read()
			htmlString = htmlBytes.decode("utf-8")
			self.feed(htmlString)
			return htmlString, self.links
		elif response.getheader('Content-Type') in ('text/html; charset=ISO-8859-15', 'text/html; charset=iso-8859-15'):
			htmlBytes = response.read()
			htmlString = htmlBytes.decode("iso-8859-1")
			self.feed(htmlString)
			return htmlString, self.links
		else:
			return "",[]

# Given a url, it tries to find the word in that url or in links from that url with a maximum of maxPages visited pages
def crawler(url, word, maxPages):  
	pagesToVisit = [url]
	visited_urls = []
	numberVisited = 0
	foundWord = False

	while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
		numberVisited = numberVisited + 1
		url = pagesToVisit[0]
		print(numberVisited, "Visiting:", url)
		
		pagesToVisit = pagesToVisit[1:]
		visited_urls.append(url)
		
		parser = LinkParser()
		data, links = parser.getLinks(url, visited_urls)
		pagesToVisit = pagesToVisit + links
		if data.find(word)>-1:
			foundWord = True
			print(" **Success!**")
	
	if foundWord:
		print("The word", word, "was found at", url)
	else:
		print("Word never found")
		
crawler("http://www.laliga.es/laliga-santander/barcelona", "10/03/1988", 1000)
