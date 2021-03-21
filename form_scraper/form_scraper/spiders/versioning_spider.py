import scrapy
import csv
import tldextract  # The module looks up TLDs in the Public Suffix List, mantained by Mozilla volunteers

from form_scraper.items import Form
class VersionSpider(scrapy.Spider):
    name = "version_scraper"

    def __init__(self, url, *args, **kwargs):
        super(VersionSpider, self).__init__(*args, **kwargs)
        self.url = url
        extracted = tldextract.extract(url)
        self.allowed_domains = '.'.join((extracted.domain, extracted.suffix))

    custom_settings = {
        'DEPTH_LIMIT': 20,
        'COOKIES_ENABLED' : False
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

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
