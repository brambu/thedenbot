import logging
import random
import feedparser
from HTMLParser import HTMLParser
import html2text

log = logging.getLogger(__name__)


def gift_fetch(url):
    try:
        feed = feedparser.parse(url)
    except BaseException as ex:
        log.error('cannot fetch from {0} ({1})'.format(url, ex))
        return 'not sure'
    maxindex = len(feed['entries']) - 1
    entry = feed['entries'][random.randint(1, maxindex)]
    return entry


def gift_print_entry(entry):
    h = HTMLParser()
    try:
        link = entry.id
        title = entry.title
        summary = h.unescape(entry.summary).encode('ascii', 'ignore')
        summary = html2text.html2text(summary)
        if 'USD' in summary:
            summary = '{0}USD'.format(summary.rsplit('USD')[0])
    except BaseException as ex:
        log.error('good: cannot parse entry {0} ({1})'.format(entry, ex))
        return 'not sure'
    return "{0} {1} {2}".format(title, summary, link)


def gift():
    urls = [
        'http://feeds.feedburner.com/ThisIsWhyImBroke?format=xml',
        'http://theworstthingsforsale.com/feed/',
        'https://www.etsy.com/shop/MugSociety29/rss'
    ]
    url = urls[random.randint(0, len(urls) - 1)]
    return gift_print_entry(gift_fetch(url))


if __name__ == "__main__":
    LOG_FORMAT = '%(asctime)s %(name)s [%(levelname)s] %(message)s'
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT)
    print gift()
