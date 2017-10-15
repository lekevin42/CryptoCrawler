import scrapy


class CryptoTalkSpider(scrapy.Spider):
    name = "cryptoTalkSpider"
    download_delay = 2
    start_urls = [
        #'https://www.cryptotalk.org/index.php?/topic/23-btc-price-speculation-thread/',
        #'https://www.cryptotalk.org/index.php?/forum/62-crypto-talk-announcements/',
        'https://www.cryptotalk.org/',
    ]


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

        for post in response.css('article.cPost.ipsBox.ipsComment.ipsComment_parent.ipsClearfix.ipsClear.ipsColumns.ipsColumns_noSpacing.ipsColumns_collapsePhone'):
            url = response.url
            postText = " ".join(post.css('div.cPost_contentWrap.ipsPad p::text').extract())
            postAuthor = post.css('a.ipsType_break::text').extract_first()
            postDate = post.css('p.ipsType_reset time::attr(title)').extract_first()
            quotedText = post.css('div.ipsQuote_contents p::text').extract_first()
            authorRep = post.css('li.ipsResponsive_hidePhone.ipsType_break::text').extract_first()
            authorPostCount = post.css('ul.cAuthorPane_info.ipsList_reset span.ipsRepBadge.ipsRepBadge_positive::text').extract()


            if not authorPostCount:
                authorPostCount = 0

            else:
                authorPostCount = authorPostCount[1].strip()

            postLikes = post.css('span.ipsReputation_count.ipsType_blendLinks.ipsType_positive::text').extract_first()

            if postLikes:
                postLikes = postLikes.strip()

            else:
                postLikes = 0

            yield {
                'url': url,
                'postText': postText,
                'postAuthor': postAuthor,
                'postDate': postDate,
                'quotedText': quotedText,
                'authorRep': authorRep,
                'authorPostCount': authorPostCount,
                'postLikes': postLikes,
            }

#post text, author, author ranking, time, quoted text, likes, first post
#17 = first post
#1139 = time

#1418 = author!, author ranking, reputation
#1476 = author date of post
#1516 = likes
#2641 = quoted text


    def getHTML(self, response, fileName):
        """
        Function to obtain HTML.
        """
        fileName += ".txt"
        with open(fileName, 'wb') as f:
            f.write(response.body)
        self.log('Saved file mainpage')
