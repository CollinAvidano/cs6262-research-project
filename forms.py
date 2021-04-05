from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from form_scraper.spiders.form_spider import FormSpider
import os
import csv
import tldextract
import subprocess

def out(command):
    output = subprocess.check_output(command, shell=True)
    return output

def check_forms(url):
    url = 'https://' + url

    ext = tldextract.extract(url)
    file_name = '.'.join((ext.domain,ext.suffix,'csv')) # basically just removing the scheme so it doesnt mess with file paths

    # oh yeah its jank... Do I care? No
    command = "scrapy crawl -a url=" + url + " form_scraper"

    print(out(command)) # actually runs scrapy from command line

    forms = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        forms = list(reader)

    # defensive measure
    if not "/" in file_name:
        os.remove(file_name)
    return forms

if __name__ == "__main__":
    print(check_forms('amazon.com'))
