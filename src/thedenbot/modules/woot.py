import feedparser
import logging
import json


log = logging.getLogger(__name__)


def woot_fetch(url, key='www'):
    result = []
    wootfeed = feedparser.parse(url)
    try:
        for entry in wootfeed['entries']:
            entrykey = \
                entry.woot_purchaseurl.split('/')[2].split('.')[0]
            if key == entrykey:
                result.append(entry)
    except BaseException as ex:
        log.warn('woot fetching error:  '
                 '{0} ({1})'.format(entry, ex))
        return
    return result


def format_result(result):
    out = []
    try:
        for entry in result:
            title = entry.title
            price = entry.woot_price
            if json.loads(entry.woot_soldout):
                purchaseurl = "Sold Out!"
            else:
                purchaseurl = entry.woot_purchaseurl
            if json.loads(entry.woot_wootoff):
                out.append("It's a woot off!")
            out.extend([title, price, purchaseurl])
            return " ".join(out)
    except BaseException as ex:
        log.warn('woot formatting parsing error: '
                 '{0} ({1})'.format(result, ex))
    return


def woot(key='www'):
    url = 'http://api.woot.com/1/sales/current.rss'
    result = woot_fetch(url, key)
    return format_result(result)
