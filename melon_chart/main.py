from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl melon_chart_top100".split())