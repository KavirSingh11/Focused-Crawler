import scraper

# query = input("Enter your topic")
query = 'html'
url = 'https://www.reddit.com/r/all/'

# url = input("Enter the starting the URL")
pageSoup = scraper.getPageData(url)
links = scraper.searchLinks
