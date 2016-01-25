from argparse import ArgumentParser
import pywapi
import sys

ctof = lambda x: int(((float(x) * 9.0 ) / 5.0 ) + 32.0)
ftoc = lambda x: int((float(x)  - 32.0) / 1.8 )
kmhtomph = lambda x: int(float(x) / 1.609344)


def weather_for_zip(zipcode):
    try:
        result = pywapi.get_weather_from_yahoo(zipcode)
    except:
        result = None
    return result

def weather_print_result(result, mode='summer'):
    try:
        title = result['condition']['title']
        text = result['condition']['text']
        tempc = result['condition']['temp']
        high = result['forecasts'][0]['high']
        low = result['forecasts'][0]['low']
        forecast = result['forecasts'][0]['text']
        windchillc = result['wind']['chill']
        windspeedkm = result['wind']['speed']
        humidity = result['atmosphere']['humidity']
        heatindex = pywapi.heat_index(float(tempc), humidity, units='metric') or ctof(tempc)
        if mode == 'winter':
            printthis = "{0} Currently {1} {2}F/{3}C  "+\
                        "Forecast: {4} (High {5}F/{6}C - Low {7}F/{8}C) "+\
                        "[Wind: chill {9}F/{10}C speed {11}mph/{12}kmh]"
            printthis = printthis.format(title, text, ctof(tempc), tempc,
                                        forecast, ctof(high), high, ctof(low), low,
                                        ctof(windchillc), windchillc, kmhtomph(windspeedkm), int(float(windspeedkm)))
        if mode == 'summer':
            printthis = "{0} Currently {1} {2}F/{3}C "+\
                        "Forecast: {4} (High {5}F/{6}C - Low {7}F/{8}C) "+\
                        "[Humidity: {9}% - Heat Index: {10}F/{11}C - Wind: {12}mph/{13}kmh]"
            printthis = printthis.format(title, text, ctof(tempc), tempc,
                                        forecast, ctof(high), high, ctof(low), low,
                                        humidity, heatindex, ftoc(heatindex), kmhtomph(windspeedkm), int(float(windspeedkm)))
    except:
        printthis = 'Not sure.'

    return printthis
