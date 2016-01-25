#!/usr/bin/env python

import logging
import random
import feedparser
from HTMLParser import HTMLParser


log = logging.getLogger(__name__)


def gift_fetch(url='http://feeds.feedburner.com/ThisIsWhyImBroke?format=xml'):
  try:
    feed = feedparser.parse(url)
  except:
    log.warn('cannot fetch from %s' % (url))
    raise RuntimeError('Feedparser error with %s' % (url))
  maxindex = len(feed['entries']) - 1
  entry = feed['entries'][random.randint(1,maxindex)]
  return entry


def gift_print_entry(entry):
  h = HTMLParser()
  try:
    link = entry.id
    title = entry.title
    summary = h.unescape(entry.summary).encode('ascii', 'ignore')
  except:
    log.error('cannot parse entry %s' % (entry))
    return 'not sure'
  return "\x02%s\x02 %s %s" % (title, summary, link)


def gift():
    return gift_print_entry(gift_fetch())