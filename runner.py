from spider import Spider

# query = input("Enter your topic")
query = 'dollar'
url = 'https://en.wikipedia.org/wiki/Main_Page'

crawler = Spider(query, url)
crawler.run()

# url = input("Enter the starting the URL")
# pageSoup = scraper.getPageData(url)
# links = scraper.searchLinks