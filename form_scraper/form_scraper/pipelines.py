# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import tldextract

class FormScraperPipeline:
    def open_spider(self, spider):
        ext = tldextract.extract(spider.url)
        file_name = '.'.join((ext.domain,ext.suffix,'csv')) # basically just removing the scheme so it doesnt mess with file paths
        print("HELLOOOOOOOOOOOOOOOOOOOOOOO")
        print(file_name)
        self.file = open(file_name, 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
