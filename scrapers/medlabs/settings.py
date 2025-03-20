# Scrapy settings for medlabs project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
###########################################################################

BOT_NAME = "medlabs"

SPIDER_MODULES = ["medlabs.spiders"]
NEWSPIDER_MODULE = "medlabs.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "medlabs (+http://www.yourdomain.com)"

# Obey robots.txt rules
#######ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "medlabs.middlewares.MedlabsSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "medlabs.middlewares.MedlabsDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "medlabs.pipelines.MedlabsPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# # Використання Splash
# SPLASH_URL = 'http://localhost:8050'
#
#
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.offsite.OffsiteMiddleware': None,  # вимикаємо OffsiteMiddleware
#     'scrapy_splash.SplashMiddleware': 725,  # Залишаємо SplashMiddleware
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 850,
#     'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 950,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 1100,
# }
# SPLASH_COOKIES_DEBUG = False
#
# SPLASH_ARGS = {
#     'wait': 3,  # Час очікування перед рендерингом сторінки
# }
#
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
# # Налаштування одночасних запитів
# CONCURRENT_REQUESTS = 16
#
# # Затримка між запитами
# DOWNLOAD_DELAY = 2
#
# # Повторні спроби запиту при невдачі
# RETRY_TIMES = 3
# LOG_LEVEL = 'DEBUG'


#
# SPIDER_MIDDLEWARES = {
#     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
# }
#
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
#
# ALLOWED_DOMAINS = ['esculab.com']
# ROBOTSTXT_OBEY = False
# OFFSITE_DOMAINS = []


# settings.py
SPLASH_URL = 'http://localhost:8050'  # Якщо ви запускаєте Splash локально
# Правильні налаштування для downloader middleware
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
# Правильні налаштування для spider middleware
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
LOG_LEVEL = 'DEBUG'
REQUEST_FINGERPRINTER_CLASS = 'scrapy_splash.SplashRequestFingerprinter'












