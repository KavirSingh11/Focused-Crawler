from linkData import linkData
from calcSim import calcSim
from bs4 import BeautifulSoup as soup
from queue import Queue
from urllib.parse import urlparse
import urllib.request
import urllib.robotparser
import bs4  

class Spider:
    startTime = 0
    endTime = 0
    urlQueue = Queue()
    query = ""
    depth = 0
    MAX_DEPTH = 2
    starting_url = ""
    robotParser = None

    def __init__(self, query, initialUrl):
        self.query = query
        self.starting_url = initialUrl 
        self.urlQueue.put(initialUrl)
        self.robotParser = urllib.robotparser.RobotFileParser()
    
    def run(self):
        self.fetchRobotsTxt()

        print("crawling...")
        while(not self.urlQueue.empty() and self.depth < self.MAX_DEPTH):
            nextUrl = self.urlQueue.get()

            if self.robotParser.can_fetch("Genji-bot/2.0", nextUrl):
                self.getUrlData(nextUrl)
            else:
                print("Cannot visit: ", nextUrl)
        
        print("Crawl depth: " + str(self.depth))

    def getUrlData(self, url):
        webpage = self.fetch(url)
        pageSoup = soup(webpage, "html.parser")
            
        title = pageSoup.title.string
        desc = self.getAttributeData(pageSoup, "meta", "description")
        author = self.getAttributeData(pageSoup, "meta", "author")
        keywords = self.getAttributeData(pageSoup, "meta", "keywords")

        links = pageSoup.find_all("a", href=True)
        # extracts url and content from <a> tag
        linkData = [self.getLinkData(link) for link in links]

        # filter relevant links
        relevantLinks = self.filterList(linkData)

        print("---- START ----")
        print("url: " + url)
        print("title: " + title)
        print("desc: " + desc)
        print("author: " + author)
        print("keywords: " + keywords)
        #print("relevant links: " + str(relevantLinks))
        print("relevant links: " + str(len(relevantLinks)))
        print("---- END ----\n")

        if len(relevantLinks) > 0:
            for rel in relevantLinks:
                nextUrl, _ = rel
                self.urlQueue.put(self.buildURL(nextUrl))
            self.depth += 1
    
    def fetchRobotsTxt(self):
        if not self.starting_url: return []

        parsed = urlparse(self.starting_url)
        domain = parsed.scheme + "://" + parsed.netloc
        url = domain + "/robots.txt"
        
        self.robotParser.set_url(url)
        self.robotParser.read()
    
    def fetch(self, url):
        if not url: return

        client = None
        webpage = None

        request = urllib.request.Request(
            url,
            data=None,
            headers={ "User-Agent": "Genji-bot/2.0" }
        )

        try:
            client = urllib.request.urlopen(request)
            webpage = client.read()
            client.close()

            return webpage
        except:
            print("Could not fetch url: " + url)
            return

    def buildURL(self, url):
        parseResult = urlparse(self.starting_url)
        formattedUrl = url

        if not url.__contains__(parseResult.scheme):
            formattedUrl = parseResult.scheme + "://" + parseResult.netloc + url

        return formattedUrl

    def getAttributeData(self, pageSoup, tag, attr):
        data = pageSoup.find(tag, attrs={ "name": attr })
        if data:
            return str(data["content"])
        else:
            return "No " + attr + " given."

    def getLinkData(self, link):
        url = link["href"]
        content =  self.getLinkDataContents(link.contents)

        return (url, content)
    
    def getLinkDataContents(self, contents):
        for content in contents:
            if isinstance(content, str):
                return content
                
    def filterList(self, links):
        print("looking for similar links")
        result = []
        simVal = 0
        select = ""

        for x in links:
            
            findSim = calcSim()
            url , text = x
            if url[-1:] == "/":
                url = url[:-1]
            parsedURL = url.split('/')[-1]
            str.replace('_', '-', parsedURL)
            parsedURL = parsedURL.split('-')

            if parsedURL is not None and text is not None and (len(parsedURL) > len(text)):
                select = ''.join(parsedURL)
           
            elif text is None: select = ''.join(parsedURL)
           
            elif parsedURL is None: select = text
           
            else:
                select = text 

            # if (len(parsedURL) > len(text)) and parsedURL is not None and text is not None:
            #     select = ''.join(parsedURL)

            # elif text is None: select =  ''.join(parsedURL)

            # elif parsedURL is None: select = text

            # else:
            #     select = text 

            simVal = findSim.urlSim(select , self.query)
            # print(simVal)
            # print(select)
            if simVal:
                result.append(x)

        return result