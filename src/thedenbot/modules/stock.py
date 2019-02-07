import urllib2
import json
import datetime
import pytz


def fetchstockinfo(search):
    apiurl = "https://api.iextrading.com/1.0/stock/{search}/quote"
    jsondata = {}
    try:
        url = apiurl.format(search=search)
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        data = res.read()
        jsondata = json.loads(data)
    except BaseException:
        pass
    return jsondata


def parse_result(result):
    if result == {}:
        return "I don't know that symbol.."

    latest_update_ms = result["latestUpdate"]
    close_time_ms = result["closeTime"]
    should_extend = False
    if latest_update_ms == close_time_ms:
        should_extend = True

    for key, value in result.items():
        if key == 'latestTime':
            continue
        if key == 'latestUpdate' or 'Time' in key:
            result[key] = format_time(value)

    printthis = "{companyName} :: {symbol}\n" \
                "{primaryExchange} :: {sector}\n" \
                "{latestUpdate} :: " \
                "{latestPrice} " \
                "{change} ({changePercent}%)"

    printthis_e = "\n[{extendedPriceTime} :: " \
                  "{extendedPrice} " \
                  "{extendedChange} ({extendedChangePercent}%)]"

    if should_extend:
        printthis += printthis_e

    try:
        return printthis.format(**result)
    except BaseException:
        return "I can't parse the result."


def format_time(epoch_ms):
    epoch_sec = epoch_ms / 1000.0
    tz = pytz.timezone('America/New_York')
    dt = datetime.datetime.fromtimestamp(epoch_sec, tz)
    return dt.strftime("%b %-d %H:%M:%S (%Z)")


def stock(searches):
    if not searches:
        return 'GOOG?'
    result = []
    for search in searches:
        search_result = fetchstockinfo(search)
        result.append(parse_result(search_result))
    return '\n\n'.join(result)


if __name__ == '__main__':
    print(stock(['AAPL', 'GOOG', 'AMZN']))
