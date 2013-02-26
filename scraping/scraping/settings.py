# Scrapy settings for scraping project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'scraping'

SPIDER_MODULES = ['scraping.spiders']
NEWSPIDER_MODULE = 'scraping.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scraping (+http://www.yourdomain.com)'

WEBSERVICE_PORT = 8181
TELNETCONSOLE_PORT = 8182

ITEM_PIPELINES = [
        'scraping.pipelines.MongoDBPipeline',
]

LOG_LEVEL = 'INFO'
LOG_FILE = 'scrapy.log'

#mongodb
MONGODB_SERVER = '10.46.24.56'
MONGODB_PORT = 27017
MONGODB_DB = 'movie'
MONGODB_COL_BASE = 'base'
MONGODB_COL_RATE = 'rate'
