import os
from multiprocessing import Process

import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from melon_chart.melon_chart.spiders.melon_chart import MelonChartSpider
from melon_chart.melon_chart.spiders.melon_chart_day import MelonChartDaySpider
from melon_chart.melon_chart.spiders.melon_chart_hot100 import MelonChartHot100Spider

settings = Settings(values={
    'BOT_NAME': "melon_chart",
    'SPIDER_MODULES': ["melon_chart.melon_chart.spiders"],
    'NEWSPIDER_MODULE': "melon_chart.melon_chart.spiders",
    'ROBOTSTXT_OBEY': False,
    'ITEM_PIPELINES': {
        "melon_chart.melon_chart.pipelines.MelonChartPipeline": 300,
        "melon_chart.melon_chart.pipelines.MongoDBWriterPipeline": 400,
        "melon_chart.melon_chart.pipelines.JsonWriterPipeline": 500,
    },
    'MONGO_URI': os.environ.get('MONGO_URI'),
    'MONGO_DATABASE': os.environ.get('MONGO_MUSIC_CHARTS_DBNAME'),
    'REQUEST_FINGERPRINTER_IMPLEMENTATION': "2.7",
    'FEED_EXPORT_ENCODING': "utf-8"
})

runner = CrawlerRunner(settings=settings)
configure_logging(settings)


def melon_chart_crawler():
    process_crawl(MelonChartSpider)

def melon_chart_hot100_crawler():
    process_crawl(MelonChartHot100Spider)

def melon_chart_day_crawler():
    process_crawl(MelonChartDaySpider)


def process_crawl(spider: scrapy.Spider):
    configure_logging(settings=settings)
    p = Process(target=crawl, args=([spider]))
    p.start()
    p.join()


def crawl(spider: scrapy.Spider):
    runner.crawl(spider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == '__main__':
    process_crawl(MelonChartSpider)
