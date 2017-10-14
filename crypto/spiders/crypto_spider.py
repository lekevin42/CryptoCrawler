import scrapy


class CryptoSpider(scrapy.Spider):
    name = "cryptospider"
    start_urls = [
        #'https://www.cryptotalk.org/index.php?/topic/23-btc-price-speculation-thread/',
        #'https://www.cryptotalk.org/index.php?/forum/62-crypto-talk-announcements/',
        'https://www.cryptotalk.org/',  #response.css('h4.ipsDataItem_title.ipsType_large.ipsType_break a::attr(href)').extract()
    ]
    keywords = {}

    with open("keywords.txt", 'r') as file:
        for keyWord in file:
            keywords[keyWord.strip()] = 0


    def parse(self, response):
        #self.getHTML(response, "frontPage")

        for topic in response.css('h4.ipsDataItem_title.ipsType_large.ipsType_break a::attr(href)').extract():
            print(topic)
            #t = response.urljoin(topic)

            yield scrapy.Request(topic, callback=self.parseTopic)


        #self.parsePost(response)
        #link.css('div.ipsType_break.ipsContained a::attr(href)').extract()

    def parseTopic(self, response):
        for t in response.css('div.ipsType_break.ipsContained a::attr(href)').extract():
            print(t)

    def parsePost(self, response):
        for post in response.css('div.ipsType_normal.ipsType_richText.ipsContained'):
            text = post.css('p::text').extract()
            for sentence in text:
                for k, v in self.keywords.items():
                    if k in sentence.lower():
                        self.keywords[k] += 1

        for k,v in self.keywords.items():
            print(k ,v)


    def getHTML(self, response, fileName):
        fileName += ".txt"
        with open(fileName, 'wb') as f:
            f.write(response.body)
        self.log('Saved file mainpage')
