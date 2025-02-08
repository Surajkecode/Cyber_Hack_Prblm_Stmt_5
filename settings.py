# settings.py

# Enable Tor proxy
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'myproject.middlewares.TorProxyMiddleware': 100,
}

# Tor proxy settings
TOR_HTTP_PROXY = 'http://127.0.0.1:9050'  # Default port for Tor's HTTP proxy