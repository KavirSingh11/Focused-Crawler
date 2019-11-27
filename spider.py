from linkData import linkData
from calcSim import calcSim
from urllib.parse import urlparse
import bs4  
import urllib.request
from bs4 import BeautifulSoup as soup

class Spider:
    startTime = 0
    endTime = 0
    urlQueue = []
    query = ""

    def __init__(self, query, initialUrl):
        self.query = query
        self.urlQueue.append(initialUrl)
    
    def run(self):
        print("crawling...")
        self.getUrlData(self.urlQueue[0])

    def getUrlData(self, url):
        client = None
        request = urllib.request.Request(
            url,
            data=None,
            headers={ "User-Agent": "Gengi-bot/2.0" }
        )

        try:
            client = urllib.request.urlopen(request)
        except:
            print('Could not visit url in queue: ' + url)
            return

        webpage = client.read()
        client.close()
            
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
        print("relevant links: " + str(relevantLinks))
        print("---- END ----")
                
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
        findSim = calcSim()

        for x in links:
            url , text = x
            if url[-1:] == "/":
                url = url[:-1]
            parsedURL = url.split('/')[-1]
            str.replace('_', '-', parsedURL)
            parsedURL = parsedURL.split('-')

            print(parsedURL)

            if parsedURL is not None and text is not None and (len(parsedURL) > len(text)):
                select = parsedURL
            elif text is None: select = parsedURL
            elif parsedURL is None: select = text
            else:
                select = text 

            simVal = findSim.urlSim(select , self.query)

            if simVal:
                result.append(x)


        return result
        