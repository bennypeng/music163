# -*- coding: utf-8 -*-

# Scrapy settings for music163 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'music163'

SPIDER_MODULES = ['music163.spiders']
NEWSPIDER_MODULE = 'music163.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'music163 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com/',
    'Pragma': 'no-cache',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'JSESSIONID-WYYY=QQTEYr3VDI7SOIGYW5mwb2wDSh\sqQvuaCvwV06osUPw8WpUG9nb/zY6rtSDe6XeXZvZ2JwC5WKm6vwcogwmeud9EZ9Whw9R5FFen7MA2HuNxcgdf7rVm4UTEIIPSbHx6kXfrst8\EFfqiwVeZ/iV6KYlz8PPpeGKx+eGcylmSgUAxG\:1547008249435; _iuqxldmzr_=32; _ntes_nnid=nlma7pglssm7j35z497y2jkgjngssvpb,1547008281416; _ntes_nuid=1547018140158.629https://music.163.com/#/song?id=13137176411440900Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36_iuqxldmzr_=32; _ntes_nnid=812037fa5714262b5f0047647b310f41,1546513097922; _ntes_nuid=812037fa5714262b5f0047647b310f41; __utmc=94650624; __utmz=94650624.1546513098.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WM_TID=9BKSvEJZToxAUFAEREZpkVZbY6YYabaF; __utma=94650624.1308687567.1546513098.1546567933.1547004716.4; WM_NI=cqqo62MFsUeeARdyhxihUzMFNNiXMj%2FhI%2BOhhQe%2Fi6xYs0ph7vkhaU4MCAQEj5bMqBLTF9J7vbk7gqefHS4If4qX%2BFYnxSmiAnrGWekc5mHTTuuWsQFYntR5DUBUCWTrY08%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb0bc21ab99fbd8c53c92bc8eb7d45a979a9faeee6d86ad8a9ad062a8be87d7e42af0fea7c3b92aa1afbf90b53a8f9abdb6e86f838eac9aeb74abb89b9bd04e8e92a7b9d062edb887ccce64ac8fabd0ec3ebc87bdd1f364f5aaa589e45ff8938da2d44faaebaeaef44a908c8adac93db6bea5d8e67ba7ba88b4b743a6ecbfb9aa4e9bb2b8b4f06383b2bea8d66fa9bdfb8ecb6098abbbb8f25b8687a295d13f888b8eb6c25d98ae97d1bb37e2a3; JSESSIONID-WYYY=G5RXADbqHdavONsM7ngjicqWK9jY4K9R8Fm9DQldxwFVIVZMB5zdaYAvGIpXgM430WrU3YxIv5lcryJoZg%5Ck30F2e%2Bc%2BI80NQJOHOgmdekg5hzYPbu29wnkY9qX%2BF12iyOhIG27%2BvmpVxAOBbxmb9vArAFzmJOpz2mU20H7uXF%2F4eAnl%3A1547018708147982:688'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'music163.middlewares.Music163SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'music163.middlewares.RandomUserAgentMiddleware': 1,
    'music163.middlewares.Music163DownloaderMiddleware': 999,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'music163.pipelines.Music163Pipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MONGO_CONFIG = {
    'host': 'localhost',
    'db': 'music163'
}

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
# LOG_STDOUT = True

#  CRITICAL - 严重错误(critical)
#  ERROR - 一般错误(regular errors)
#  WARNING - 警告信息(warning messages)
#  INFO - 一般信息(informational messages)
#  DEBUG - 调试信息(debugging messages)
LOG_LEVEL = "INFO"
# LOG_FILE = "mySpider.log"
