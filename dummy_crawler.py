from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse
import re
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request

# Reimplementing HTMLParser to handle tags
class LinkParser(HTMLParser):

        def handle_starttag(self, tag, attrs):
                # Handling anchors
                if tag == 'a':
                        for (key, value) in attrs:
                                if key == 'href':
                                        newUrl = parse.urljoin(self.baseUrl, value)
                                        # Add to new links if it hasn't been visited yet
                                        if newUrl.startswith("http") and newUrl not in self.visited_urls and newUrl not in self.links:
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
                request = Request(url, headers={"Connection" : "close", "User-Agent" : "Googlebot/2.1 (+http://www.google.com/bot.html)"})
                try:
                        response = urlopen(request)
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
                except HTTPError as e:
                        print(e.code)
                        #print(e.read())
                        return "",[]
                except URLError as e:
                    if hasattr(e, 'reason'):
                        print('We failed to reach a server.')
                        print('Reason: ', e.reason)
                    elif hasattr(e, 'code'):
                        print('The server couldn\'t fulfill the request.')
                        print('Error code: ', e.code)
                    return "",[]
                except UnicodeEncodeError:
                        return "",[]
                except UnicodeDecodeError:
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
                        pagesToVisit = pagesToVisit[1:]
                        visited_urls.append(url)
                        print(numberVisited, "Current page:", url)

                        parser = LinkParser()
                        data, links = parser.getLinks(url, visited_urls)
                        pagesToVisit = pagesToVisit + list(set(links) - set(pagesToVisit))
                                                
                        result = prog.match(url)
                        if result:
                                print("Searching in:", url)
                                if data.find(word)>-1:
                                        foundWord = True
                                        print(" **Success!**")
                        numberVisited = numberVisited + 1
                
                if foundWord:
                        print("The word", word, "was found at", url)
                else:
                        print("Word never found")
                                
# Given a url, it tries to find pages that much urlpattern in the links from that url with a maximum of maxPages visited pages
def crawler2(url, urlpattern, maxPages):  
                pagesToVisit = [url]
                found_urls = []
                numberFound = 0

                prog = re.compile(urlpattern)

                while numberFound < maxPages and pagesToVisit != []:
                                
                        url = pagesToVisit[0]
                        pagesToVisit = pagesToVisit[1:]
                        
                        #print("Visiting:", url)

                        result = prog.match(url)
                        if result and url not in found_urls:
                                numberFound = numberFound + 1
                                print(numberFound, "Found:", url)
                                found_urls.append(url)  
                        
                        parser = LinkParser()
                        data, links = parser.getLinks(url, found_urls)
                        pagesToVisit = pagesToVisit + list(set(links) - set(pagesToVisit))
                

