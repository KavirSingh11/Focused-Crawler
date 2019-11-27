import scraper

query = input("Enter your topic")

url = input("Enter the starting the URL")
pageSoup = scraper.getPageData(url)
links = scraper.searchLinks
