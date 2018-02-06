import urllib2
import json


def fetchstockinfo(search):
    apiurl = 'http://www.google.com/finance/info?q='
    jsondata = {}
    try:
        url = apiurl + search
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        data = res.read()
        data = data.replace('\n', '').split('//')[1].strip()
        jsondata = json.loads(data)
    except BaseException:
        pass
    return jsondata


def parse_result(result):
    if result == {}:
        return "I don't know that symbol.."
    # NASDAQ:GOOG Aug 1, 4:00PM EDT :: 904.22 +16.47 (1.86%)
    printthis = "{e}:{t} {lt} :: {l} {c} ({cp}%)"
    printthis_e = " [ {elt} :: {el} {ec} ({ecp}%) ]"
    for entry in result:
        if 'el' in entry:
            printthis += printthis_e
        try:
            return printthis.format(**entry)
        except BaseException:
            return "I can't parse the result."


def stock(searches):
    if not searches:
        return 'GOOG?'
    result = []
    for search in searches:
        search_result = fetchstockinfo(search)
        result.append(parse_result(search_result))
    return '\n'.join(result)
