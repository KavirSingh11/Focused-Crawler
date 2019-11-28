
from spider import Spider

# query = input("Enter your topic")
query = 'trump'
url = 'https://www.reddit.com/r/all/'

crawler = Spider(query, url)
crawler.run()

# url = input("Enter the starting the URL")
# pageSoup = scraper.getPageData(url)
# links = scraper.searchLinks