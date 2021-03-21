import scrapy
import csv

from form_scraper.items import Form
class FormSpider(scrapy.Spider):
    name = "form_scraper"

    # def __init__(self, url_csv='urls.csv', depth_max=20, *args, **kwargs):
    def __init__(self, url_csv='urls.csv', *args, **kwargs):
        super(FormSpider, self).__init__(*args, **kwargs)
        self.url_csv = url_csv
        # self.depth_max = depth_max

    custom_settings = {
        'DEPTH_LIMIT': 20,
        'COOKIES_ENABLED' : False
    }

    def start_requests(self):
        urls = []
        print("here")
        with open(self.url_csv, newline='') as f:
            reader = csv.reader(f)
            urls = list(reader)
            print("reader", urls)
        for url in urls:
            print(url)
            yield scrapy.Request(url=url[0], callback=self.parse)
            # yield scrapy.Request(url=url[0], callback=self.parse, cb_kwargs=dict(depth=0))

    # def parse(self, response, depth):
    def parse(self, response):
        for meta in response.xpath("//meta[@name='generator']@content").getall():
            yield meta

        for script in response.xpath("//script").getall():
            if script.startswith('_W.configDomain = "www.weebly.com";'):
                yield "Weebly"
            elif script.startswith('var Shopify = Shopify || {{}};'):
                yield "Shopify"

        if response.text.contains("<!-- This is Squarespace. -->"):
            yield "Squarespace"

        for next_page in response.css('a::attr(href)'):
            if next_page is not None:
                next_page_url = response.urljoin(next_page.extract())
                yield response.follow(next_page_url, callback=self.parse)
                # should only follow if the url is in the original domain
                # setting class var allowed_domains list may also do this
                # if you add this later use the should follow middle ware example here
                # https://stackoverflow.com/questions/53547246/scrapy-follow-external-links-only
                # yield response.follow(url, callback=self.parse,cb_kwargs=dict(depth=depth+1))
