class linkData:

    def __init__(self, keywords, desc, title, linkURL):
        keywordList = []


        self.keywords = keywords
        self.desc = desc
        self.title = title
        self.linkURL = linkURL

        urlParse = linkURL.split("/")
        str.replace('_' , '-', urlParse)
        keywordList.append(keywords.split() +" "+ desc.split() +  " " +title.split + " " + urlParse[-1].split('-'))