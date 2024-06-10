import scrapy


class DressesSpider(scrapy.Spider):
    """
    Spider to scrape products from all the categories under women clothing 
    """
    name = "dresses"
    allowed_domains = ["ebay.com"]
    start_urls = [
        "https://www.ebay.com/b/Womens-Tops/53159/bn_661824",
        'https://www.ebay.com/b/Womens-Dresses/63861/bn_661850',
        'https://www.ebay.com/b/Womens-Coats-Jackets-Vests/63862/bn_661792',
        'https://www.ebay.com/b/Womens-Intimates-Sleep/11514/bn_661761',
        'https://www.ebay.com/b/Womens-Sweaters/63866/bn_661855',
        'https://www.ebay.com/b/Womens-Pants/63863/bn_661852',
        'https://www.ebay.com/b/Womens-Jeans/11554/bn_661774',
        'https://www.ebay.com/b/Womens-Skirts/63864/bn_661853'



    ]

    def parse(self, response):
        """
        Function to handle the urls 

        """
        product_info = response.css('div.s-item__wrapper')

        image_url = product_info.css(
            'div img.s-item__image-img::attr(src)').get()
        title = product_info.css('h3.s-item__title::text').get()
        price = product_info.css('span.s-item__price::text').get()
        shipping_cost = product_info.css('span.s-item__shipping::text').get()

        yield {
            'image_url': image_url,
            'title': title,
            'price': price,
            'shipping_cost': shipping_cost
        }

        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
