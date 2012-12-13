#!/usr/bin/python

import re
import os
from datetime import date

from scrapy import log
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawler.spiders import LinkSpider

#log.start()

spider = LinkSpider()
overrides = {
    'LOG_ENABLED': True,
    'LOG_LEVEL': 'DEBUG',
    'LOG_STDOUT': True,
    'DOWNLOAD_DIR' : os.path.dirname(__file__) + '/files',
    'ITEM_PIPELINES': [ 'crawler.pipelines.LinkPipeline' ],
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,
        'crawler.middlewares.LinkRedirectMiddleware': 100,
    },
    'CONCURRENT_REQUESTS': 36,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 36,
    'CONCURRENT_ITEMS': 300
}
settings = get_project_settings()
settings.overrides.update(overrides)
crawler = CrawlerProcess(settings)
crawler.install()
crawler.configure()
crawler.crawl(spider)
crawler.start()
