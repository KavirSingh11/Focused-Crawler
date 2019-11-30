from spider import Spider

defaultUrl = 'https://www.reddit.com/r/all/'
initialUrl = defaultUrl

urlInput = input("Enter a starting url: ")
queryInput = input("Enter your topic: ")

if len(urlInput) > 0:
    initialUrl = urlInput

crawler = Spider(queryInput, initialUrl)
crawler.run()
