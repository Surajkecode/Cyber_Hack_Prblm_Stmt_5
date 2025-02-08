# middlewares.py

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from urllib.parse import urlparse
import os

from my_project.my_project.settings import TOR_HTTP_PROXY

class TorProxyMiddleware(HttpProxyMiddleware):
    def process_request(self, request, spider):
        request.meta['proxy'] = TOR_HTTP_PROXY