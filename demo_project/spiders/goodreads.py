import scrapy
from scrapy.loader import ItemLoader
from demo_project.items import QuoteItem


class GoodReadsSpider(scrapy.Spider):
    # identity
    name = 'goodreads'
    # requests

    def start_requests(self):
        url = 'https://www.goodreads.com/quotes?page=1'
        # urls = [
        #     'https://www.goodreads.com/quotes?page=1',
        #     'https://www.goodreads.com/quotes?page=2',
        #     'https://www.goodreads.com/quotes?page=3',
        #     'https://www.goodreads.com/quotes?page=4',
        #     'https://www.goodreads.com/quotes?page=5',
        #     'https://www.goodreads.com/quotes?page=6',
        #     'https://www.goodreads.com/quotes?page=7',
        #     'https://www.goodreads.com/quotes?page=8',
        #     'https://www.goodreads.com/quotes?page=9',
        #     'https://www.goodreads.com/quotes?page=10',

        # ]
        # for url in urls:
        yield scrapy.Request(url=url, callback=self.parse)
    # response

    def parse(self, response):
        for quote in response.selector.xpath("//div[@class='quote']"):
            loader = ItemLoader(
                item=QuoteItem(), selector=quote, response=response)
            loader.add_xpath('text', ".//div[@class='quoteText']/text()[1]")
            loader.add_xpath(
                'author', ".//div[@class='quoteText']/child::span/text()")
            loader.add_xpath(
                'tags', ".//div[@class='greyText smallText left']/a/text()")
            yield loader.load_item()
            # yield {
            #     'text' : quote.xpath(".//div[@class='quoteText']/text()[1]").extract_first(),
            #     'author' : quote.xpath(".//div[@class='quoteText']/child::span/text()").extract_first(),
            #     'tags' : quote.xpath(".//div[@class='greyText smallText left']/a/text()").extract()

            # }
        next_page = response.selector.xpath(
            "//a[@class = 'next_page']/@href").extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
        # page_number = response.url.split("=")[1]
        # _file = "{0}.html".format(page_number)
        # with open(_file, 'wb') as f:
        #     f.write(response.body)
