import re
import os
from urllib import unquote
from urlparse import urlparse, urljoin
from datetime import datetime

from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.utils.url import canonicalize_url

from crawler.items import LinkItem

class LinkSpider(BaseSpider):

    def __init__(self, *args, **kwargs):
        self.projects = []
        self.visited = []
        self.website = 'http://translate.wordpress.org'
        self.allowed_domains = [ 'translate.wordpress.org' ]
        self.url = self.website
        self.start_urls = [ self.website ]

    def get_urls(self, response):

        if not hasattr(response, 'body_as_unicode'):
            return []

        hxs = HtmlXPathSelector(response)
        urls = []

        # Common href in anchors
        for url in [ u.extract() for u in hxs.select('//a/@href') ]:
            urls.append(canonicalize_url(urljoin(self.url, url)))

        return list(set(urls))


    def parse(self, response):

        urls = self.get_urls(response)
        nurls = []

        # Remove GET params
        for url in urls:
            u = re.sub(r'\?.*', '', url)
            nurls.append(u)

        urls = list(set(nurls))
        nurls = []

        # Remove login URL
        r_login = re.compile('.*/login.*')
        for url in urls:
            if not r_login.match(url):
                nurls.append(url)

        urls = list(set(nurls))
        nurls = []

        # Remove already downloaded project links
        r_project = re.compile('projects/(?P<project>.*)')
        for url in urls:
            if not r_project.match(url):
                nurls.append(url)

        urls = list(set(nurls))
        nurls = []

        # PO files export, send to pipeline and remember project
        r_export_link = re.compile('.*export-translations$')
        for url in urls:
            if r_export_link.match(url):
                s = r_project.search(url)
                p = s.group('project')
                if p in self.projects:
                    continue
                elif len(p) > 0 and p not in self.projects:
                    self.projects.append(p)
                    self.projects = list(set(self.projects))
                yield LinkItem(
                    project = p,
                    url = url)

        # Continue crawling
        for url in urls:

            # Don't crawl already downloaded URLs
            if url in self.visited:
                continue
            else:
                self.visited.append(url)
                self.visited = list(set(self.visited))

            # Don't crawl already downloaded projects
            for p in self.projects:
                if p in url:
                    continue

            # Make a request only to check response headers
            #request = Request(url = url, callback = self.parse, method = 'HEAD')
            #request.meta.setdefault('parent_response', response)
            #request.meta.setdefault('check_head', response)
            request = Request(url = url, callback = self.parse, method = 'GET')
            yield request
