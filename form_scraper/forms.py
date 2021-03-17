from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from form_scraper.spiders.form_spider import FormSpider
import os

process = CrawlerProcess(get_project_settings())

process.crawl('form_scraper', url_csv=os.path.abspath('urls.csv'), depth_max=20)
process.start() # the script will block here until the crawling is finished
