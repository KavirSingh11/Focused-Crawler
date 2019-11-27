import bs4  
from urllib.request import urlopen as uReq
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