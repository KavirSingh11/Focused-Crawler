from bs4 import BeautifulSoup as soup
from queue import Queue
from urllib.parse import urlparse
import urllib.request
import urllib.robotparser
import bs4 
import time
import re

class Spider:
    startTime = 0
    endTime = 0
    urlQueue = Queue()
    query = ""
    depth = 0
    MAX_DEPTH = 10
    starting_url = ""
    robotParser = None
    name = "Genji-bot/2.0"
    visitHistory = []

    crawlResults = []

    def __init__(self, query, initialUrl):
        self.query = query
        self.starting_url = initialUrl 
        self.urlQueue.put(initialUrl)
        self.robotParser = urllib.robotparser.RobotFileParser()
    
    def run(self):
        startTime = time.time()

        print("beginning crawl...")
        while(not self.urlQueue.empty() and self.depth < self.MAX_DEPTH):
            nextUrl = self.urlQueue.get()
            self.fetchRobotsTxt(nextUrl)

            crawlDelay = self.robotParser.crawl_delay(self.name)

            hasVisitedLink = nextUrl in self.visitHistory
            if (hasVisitedLink):
                continue

            canVisitLink = self.robotParser.can_fetch(self.name, nextUrl)

            if canVisitLink:
                if crawlDelay:
                    time.sleep(crawlDelay * 1000) # crawlDelay is in seconds, sleep accepts milliseconds

                self.crawl(nextUrl)
                self.visitHistory.append(nextUrl)
            else:
                print("Cannot visit: ", nextUrl)
        
        endTime = time.time()
        crawlTime = endTime - startTime

        print("Crawl depth: " + str(self.depth))

        self.save(crawlTime)

    def save(self, crawlTime):
        print("saving results...")
        file = open("results.txt", "w", encoding="utf-8")

        totalSize = 0
        resultToSave = ""


        for result in self.crawlResults:
            url, title, desc, author, keywords, size, links = result
            totalSize += size
            
            line = "URL: " + url + "\n" \
                + "TITLE: " + title + "\n" \
                + "DESCRIPTION: " + desc + "\n" \
                + "KEYWORDS: " + str(keywords) + "\n" \
                + "SIZE: " + str(size) + " bytes\n" \
                + "RELEVANT LINKS: " + str(links) + "\n" \
                + "----------------------------------------\n"
            
            resultToSave += line
                
        
        resultToSave += "\nTOTAL BYTES CRAWLED: " + str(totalSize) + " byte (s)\n" \
            + "TOTAL CRAWL TIME: " + str(round(crawlTime, 5)) + " second (s)"
        file.write(resultToSave)
        file.close()

    def crawl(self, url):
        print("crawling " + url)
        webpage = self.fetch(url)
        
        if webpage is None:
            finalResult = ( \
                url, \
                "No title given.", \
                "No description given.", \
                "No author given.", \
                "No keywords given.", \
                0, \
                [] \
            )
            self.crawlResults.append(finalResult)
            return

        pageSoup = soup(webpage, "html.parser")
            
        title = "No title given."
        if pageSoup.title:
            title = pageSoup.title.string

        desc = self.getAttributeData(pageSoup, "meta", "description")
        author = self.getAttributeData(pageSoup, "meta", "author")
        keywords = self.getAttributeData(pageSoup, "meta", "keywords")
        webpageSize = webpage.__len__()

        links = pageSoup.find_all("a", href=True)
        # extracts url and content from <a> tag
        linkData = [self.getLinkData(link) for link in links]

        # filter relevant links
        relevantLinks = self.filterList(linkData)
        
        finalResult = (url, title, desc, author, keywords, webpageSize, str(relevantLinks))
        self.crawlResults.append(finalResult)
    
        if len(relevantLinks) > 0:
            for link in relevantLinks:
                self.urlQueue.put(link)
            self.depth += 1

    def fetchRobotsTxt(self, url):
        parsed = urlparse(url)
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
            headers={ "User-Agent": self.name }
        )

        try:
            client = urllib.request.urlopen(request)
            if client.getcode() > 400:
                raise
            webpage = client.read()
            client.close()

            return webpage
        except:
            print("Could not fetch url: " + url)
            return

    def buildURL(self, url):
        parseResult = urlparse(self.starting_url)
        formattedUrl = url

        isInvalidUrl = not url.__contains__("http")

        if isInvalidUrl:
            formattedUrl = parseResult.scheme + "://" + parseResult.netloc + url

        return formattedUrl

    def getAttributeData(self, pageSoup, tag, attr):
        data = pageSoup.find(tag, attrs={ "name": attr })
        if data and "content" in data:
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
        relevantLinks = []
        results = []
        wordsInQuery = list(dict.fromkeys(self.query.split(" ")))
        similarityThreshold = len(wordsInQuery) / 2 #should contain more than half the words


        for x in links:
            url , text = x
            # remove trailing /
            if url[-1:] == "/":
                url = url[:-1]
            
            path = urlparse(url).path
            wordsInPath = path.split("/")

            # Asssumption: website title is the last element in path
            websiteTitle = wordsInPath[-1]
            normalizedTitle = websiteTitle.replace('_', '-')
            wordsInTitle = normalizedTitle.split("-")

            wordsInText = []
            if text is not None:
                wordsInText = text.split(" ")

            allWordsFromLink = list(dict.fromkeys(wordsInTitle + wordsInText))

            intersection = list(set(wordsInQuery) & set(allWordsFromLink))

            if len(intersection) >= similarityThreshold:
                relevantLinks.append(x)

        for rel in relevantLinks:
            nextLink, _ = rel
            nextValidLink = self.buildURL(nextLink)
            results.append(nextValidLink)

        
        resultsWithoutDuplicates = list(dict.fromkeys(results))
        return resultsWithoutDuplicates