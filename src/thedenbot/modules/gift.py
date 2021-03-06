import logging
import random
import feedparser
import html
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
    try:
        link = entry.id
        title = entry.title
        summary = html.unescape(entry.summary).encode('utf-8', 'ignore')
        summary = summary.decode('utf-8')
        summary = html2text.html2text(summary)
        if 'USD' in summary:
            summary = '{0}USD'.format(summary.rsplit('USD')[0])
    except BaseException as ex:
        log.error('good: cannot parse entry {0} ({1})'.format(entry, ex))
        return 'not sure'
    return u"{0} {1} {2}".format(title, summary, link)


def gift():
    urls = [
        'http://theworstthingsforsale.com/feed/',
    ]
    # url = urls[random.randint(0, len(urls) - 1)]
    url = urls[0]
    return gift_print_entry(gift_fetch(url))


if __name__ == "__main__":
    LOG_FORMAT = '%(asctime)s %(name)s [%(levelname)s] %(message)s'
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT)
    print(gift())
