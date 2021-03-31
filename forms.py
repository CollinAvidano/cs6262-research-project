from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from form_scraper.spiders.form_spider import FormSpider
import os
import csv
import tldextract

# MUST BE CALLED WITH URL INCLUDING SCHEME (https://)
def check_forms(url):
    url = 'https://' + url
    process = CrawlerProcess(get_project_settings())
    process.crawl('form_scraper', url=url, depth_max=20)
    process.start()  # the script will block here until the crawling is finished
    ext = tldextract.extract(url)
    file_name = '.'.join((ext.domain,ext.suffix,'csv')) # basically just removing the scheme so it doesnt mess with file paths

    forms = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        forms = list(reader)
    os.remove(file_name)
    return forms

if __name__ == "__main__":
    print(check_forms('amazon.com'))
