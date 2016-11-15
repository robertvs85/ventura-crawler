from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse
import re
from urllib.error import HTTPError

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
		try:
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
		except HTTPError:
			return "",[]

# Given a url, it tries to find the word in that url or in links from that url with a maximum of maxPages visited pages
def crawler(url, urlpattern, word, maxPages):  
		pagesToVisit = [url]
		visited_urls = []
		numberVisited = 0
		foundWord = False

		prog = re.compile(urlpattern)

		while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
				
			url = pagesToVisit[0]
			result = prog.match(url)
			
			pagesToVisit = pagesToVisit[1:]
			visited_urls.append(url)
			print(url)

			if result:
				print(numberVisited, "Visiting:", url)
			
			parser = LinkParser()
			data, links = parser.getLinks(url, visited_urls)
			pagesToVisit = pagesToVisit + links
			if result and data.find(word)>-1:
				foundWord = True
				print(" **Success!**")
			numberVisited = numberVisited + 1
		
		if foundWord:
			print("The word", word, "was found at", url)
		else:
			print("Word never found")
				
