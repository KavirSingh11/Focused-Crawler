import bs4  
from urllib.request import urlopen
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
        try:
            client = urlopen(url)
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
            relevantLinks = linkData

            print("---- START ----")
            print("url: " + url)
            print("title: " + title)
            print("desc: " + desc)
            print("author: " + author)
            print("keywords: " + keywords)
            print("relevant links: " + str(relevantLinks))
            print("---- END ----")
        except:
            print('Could not visit url.')
        finally:
            if client != None:
                client.close()
                
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
        


