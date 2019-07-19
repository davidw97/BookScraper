from scrapy.spiders import Spider
from ..items import BookItem, AuthorItem
import json
import re


class WikiBookSpider(Spider):
    """
    Spider to get basic information about a book from a wikipedia article
    """
    name = 'WikiBookSpider'

    start_urls = ["file:///home/david/Desktop/Mockingbird%20-%20Wikipedia.html"]

    def parse(self, response):
        item = BookItem()

        table_rows = response.css('table.infobox.vcard').xpath('./tbody/tr')

        # url (For reference and to prevent duplicates)
        item['url'] = response.url

        # Title
        item['title'] = response.xpath('string(//h1[@id="firstHeading"])').get()

        # Place unknown values into a list
        other = {}
        unknown = []

        # Details from infobox
        for tr in table_rows:
            # Get main image from the article, if it exists
            if tr.xpath('./td/a[@class="image"]/@href'):
                item['image'] = tr.xpath('./td/a[@class="image"]/@href').get()
            else:
                data = tr.xpath('string(./td)').get()
                title = tr.xpath('./th/text()').get()

                try:
                    if title is not None:
                        new_title = re.sub(r' ', '_', title.lower())
                        item[new_title] = data
                except (KeyError):
                    other[new_title] = data
                except (AttributeError):
                    unknown.append(data)

        # Description from top section in article
        item['description'] = "".join([
            p.xpath('string()').get()
            for p in response.xpath('//*[@id="toc"]/preceding-sibling::p')
        ])

        other['unknown'] = unknown
        item['other'] = json.dumps(other)

        yield item


class WikiAuthorSpider(Spider):
    """
    Spider to get basic information about a book from a wikipedia article
    """
    name = 'WikiAuthorSpider'

    start_urls = ["file:///home/david/Desktop/James%20A.%20Michener%20-%20Wikipedia.html"]

    def parse(self, response):
        item = AuthorItem()

        table_rows = response.css('table.infobox.vcard').xpath('./tbody/tr')

        # url (For reference and to prevent duplicates)
        item['url'] = response.url

        # Title
        item['name'] = response.xpath('string(//h1[@id="firstHeading"])').get()

        # Place unknown values into a list
        other = {}
        unknown = []

        # Details from infobox
        for tr in table_rows:
            # Get main image from the article, if it exists
            if tr.xpath('./td/a[@class="image"]/@href'):
                item['image'] = tr.xpath('./td/a[@class="image"]/@href').get()
            else:
                data = tr.xpath('string(./td)').get()
                title = tr.xpath('./th/text()').get()

                try:
                    if title is not None:
                        new_title = re.sub(r' ', '_', title.lower())
                        item[new_title] = data
                except (KeyError):
                    other[new_title] = data
                except (AttributeError):
                    unknown.append(data)

        # Description from top section in article
        item['description'] = "".join([
            p.xpath('string()').get()
            for p in response.xpath('//*[@id="toc"]/preceding-sibling::p')
        ])

        other['unknown'] = unknown
        item['other'] = json.dumps(other)

        yield item