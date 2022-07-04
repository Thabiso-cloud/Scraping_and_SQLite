import scrapy
from ..items import TilesInfoItem
from scrapy.loader import ItemLoader

class TilesSpider(scrapy.Spider):
    name = 'tiles'
    allowed_domains = ['www.magnatiles.com']
    start_urls = ['http://www.magnatiles.com/products/page/1/']

    def parse(self, response):

        for p in response.css('ul.products li'):
            il = ItemLoader(item=TilesInfoItem(), selector=p)

            il.add_css('sku', 'a.button::attr(data-product_sku)')
            il.add_css('name', 'h2::text')
            il.add_css('price', 'span.price bdi::text')

            yield il.load_item()
            # yield {
            # 'name': p.css('h2::text').get(),
            # 'sku': p.css('a.button::attr(data-product_sku)').get(),
            # 'price': p.css('span.price bdi::text').get(),
            # }

        next_page = response.css('ul.page-numbers a.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
