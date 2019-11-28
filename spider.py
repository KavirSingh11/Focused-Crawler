from linkData import linkData
from calcSim import calcSim
from urllib.parse import urlparse
import bs4  
import urllib.request
from bs4 import BeautifulSoup as soup
from queue import Queue

class Spider:
    startTime = 0
    endTime = 0
    urlQueue = Queue()
    query = ""
    depth = 0
    MAX_DEPTH = 2
    starting_url = ""

    def __init__(self, query, initialUrl):
        self.query = query
        self.starting_url = initialUrl 
        self.urlQueue.put(initialUrl)
    
    def run(self):
        print("crawling...")
        while(not self.urlQueue.empty() and self.depth < self.MAX_DEPTH):
            self.getUrlData(self.urlQueue.get())
        
        print("depth: " + str(self.depth))

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
            print ("Could not visit url in queue: " + url)
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
        #print("relevant links: " + str(relevantLinks))
        print("---- END ----")

        for rel in relevantLinks:
            nextUrl, _ = rel
            if(not nextUrl.__contains__("http")):
                nextUrl = self.buildURL(nextUrl)
            self.urlQueue.put(nextUrl)
            
            
        
        self.depth += 1

    def buildURL(self, url):

        parseResult = urlparse(self.starting_url)
        if not url.__contains__(parseResult.scheme):
            url = parseResult.scheme + "://" + parseResult.netloc + url

        print(url)

        return url


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