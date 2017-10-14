import scrapy


class CryptoSpider(scrapy.Spider):
    name = "cryptospider"
    download_delay = 2
    start_urls = [
        #'https://www.cryptotalk.org/index.php?/topic/23-btc-price-speculation-thread/',
        #'https://www.cryptotalk.org/index.php?/forum/62-crypto-talk-announcements/',
        'https://www.cryptotalk.org/',
    ]
    #keywords = {}

    #with open("keywords.txt", 'r') as file:
    #    for keyWord in file:
    #        keywords[keyWord.strip()] = 0


    def parse(self, response):
        """
        Main parsing function used for scrapy.
        Grab all the topics from cryptotalk using scrapy and use a scrapy request to iterate through the list.
        Use parseTopic function as a callback for the request.
        """
        #self.getHTML(response, "frontPage")

        for topic in response.css('h4.ipsDataItem_title.ipsType_large.ipsType_break a::attr(href)').extract():
            print(topic)
            yield scrapy.Request(topic, callback=self.parseTopic)


    def parseTopic(self, response):
        """
        Parse through the topic to get individual subtopics and use scrapy request once again with
        parsePost to obtain individual posts.
        """

        for subtopic in response.css('div.ipsType_break.ipsContained a::attr(href)').extract():
            print(subtopic)
            yield scrapy.Request(subtopic, callback=self.parsePost)


    def parsePost(self, response):
        """
        Parse through the post list and then search for keywords and increment the frequency (in a dictionary)
        when it appears.
        """
        for post in response.css('div.ipsType_normal.ipsType_richText.ipsContained'):
            text = post.css('p::text').extract()
            #for sentence in text:
            #    for k, v in self.keywords.items():
            #        if k in sentence.lower():
            #            self.keywords[k] += 1

#post text, author, author ranking, time, quoted text, likes, first post
#17 = first post
#1139 = time

#1418 = author, author ranking, reputation
#1476 = author date of post
#1516 = likes
#2641 = quoted text

        yield {
            'url': response.url,
            'text': text
        }


    def getHTML(self, response, fileName):
        """
        Function to obtain HTML.
        """
        fileName += ".txt"
        with open(fileName, 'wb') as f:
            f.write(response.body)
        self.log('Saved file mainpage')
