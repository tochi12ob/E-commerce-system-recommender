import scrapy


class AmazonProductSpider(scrapy.Spider):
    name = 'amazon_product'
    start_urls = ['https://www.amazon.com/s?k=womens+dresses',
                  'https://www.amazon.com/s?k=Tops']

    def parse(self, response):
        products = response.css('.s-result-item')

        for product in products:
            product_info = {
                'title': product.css('.s-line-clamp-2 > a ::text').get(),
                'url': product.css('.s-line-clamp-2 > a ::attr(href)').get(),
                'image_url': product.css('.s-image ::attr(src)').get(),
                'ratings': product.css('.s-star-rating ::text').get(),
                'ratings_count': product.css('span[aria-label*="ratings"] ::text').get(),
                'price': product.css('.a-price > .a-offscreen ::text').get(),
                'delivery_info': product.css('.s-align-children-center > .a-row:last-child ::text').get()
            }
            yield product_info

        next_page = response.css('a.s-pagination-next ::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
