#NOTE when importing click ctrl-shift-p and type python interpreter and make sure the one selected is python 3.8 64 bit, otherwise imports dont work

import bs4  
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

class pageData:

    keywordList = []

    def __init__(self, keywords, desc, title, linkURL, linkText):
        self.keywords = keywords
        self.desc = desc
        self.title = title
        self.linkURL = linkURL
        self.linkText = linkText
        pageData.keywordList.append(keywords.split())
        
    def printKeywords(self):
        print("Keywords are : " + self.keywords)

    def printDesc(self):
        print("Description is : " + self.desc)

def getPageData(url):

    uClient = uReq(url)
    webpage = uClient.read()
    uClient.close()

    pageSoup = soup(webpage , "html-parser")
    title = pageSoup.title.string
    print(title)

    desc = pageSoup.find(attrs={'name' : 'Description'})
    if desc == None:
        desc = pageSoup.find(attrs={'name' : 'description'})
    #print(desc['content'])

    keywords = pageSoup.find(attrs={'name' : 'keywords'})
    #print(keywords['content'])


    linksURL = ""
    linkText = ""
    for a in pageSoup.find_all('a', href=True, text=True):
        linksURL = a['href']
        linkText = a['text']

    pageInfo = pageData(keywords['content'] , desc['content'], title, linksURL, linkText)

    pageInfo.printKeywords()
    pageInfo.printDesc()

    
    return pageSoup

def searchLinks(pageSoup):
    print("yeet")



#keywords = pageSoup.findAll("title" , )


#step 1. find all text and titles of <a> tags
#step 2. sort through the text and look for most similar, go to url with highest score
