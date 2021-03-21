import scrapy
import csv
import tldextract  # The module looks up TLDs in the Public Suffix List, mantained by Mozilla volunteers

from form_scraper.items import Form
class FormSpider(scrapy.Spider):
    name = "form_scraper"

    def __init__(self, url, *args, **kwargs):
        super(FormSpider, self).__init__(*args, **kwargs)
        self.url = url
        extracted = tldextract.extract(url)
        self.allowed_domains = '.'.join((extracted.domain, extracted.suffix))

        custom_settings = {
        'DEPTH_LIMIT': 20,
        'COOKIES_ENABLED' : False
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        for form in response.css('input'):
            form_item = Form()
            form_item['url'] = response.url
            form_item['given_class'] = form.attrib.get('class',"")
            form_item['given_type'] = form.attrib.get('type',"")
            yield form_item

        for form in response.css('form'):
            form_item = Form()
            form_item['url'] = response.url
            form_item['given_class'] = form.attrib.get('class',"")
            form_item['given_type'] = form.attrib.get('type',"")
            yield form_item

        for next_page in response.css('a::attr(href)'):
            if next_page is not None:
                next_page_url = response.urljoin(next_page.extract())
                yield response.follow(next_page_url, callback=self.parse)
                # should only follow if the url is in the original domain
                # setting class var allowed_domains list may also do this
                # if you add this later use the should follow middle ware example here
                # https://stackoverflow.com/questions/53547246/scrapy-follow-external-links-only
