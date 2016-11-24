from datetime import datetime, timedelta

import forecastio
from geopy.geocoders import Nominatim


def ftoc(x):
    return int((float(x) - 32.0) / 1.8)


def mphtokph(x):
    return x * 1.60934


def weather_for_input(input, token=None):
    geolocator = Nominatim(country_bias='US')
    location = geolocator.geocode(input)
    ret = forecastio.load_forecast(token,
                                   location.latitude,
                                   location.longitude,
                                   units='us')
    result = ret.json
    return location.address, result


def weather_print_result(address, result):
    args = {}
    args.update(**result)
    args.update(address=address)

    template = [
        u'Weather for {address}',
        u'{current_time} {timezone}',
        u'',
        u'Currently: {currently[summary]} '
        u'{currently[temperature]:0.0f}\u00b0F/{current_temperature_c}\u00b0C '
        u'Feels like: {currently[apparentTemperature]:0.0f}\u00b0F'
        u'/{feels_like_c}\u00b0C',
        u'humidity: {humidity_pct}%, wind: {currently[windSpeed]}mph'
        u'/{wind_kph:.2f}kph',
        u'High: {daily[data][0][temperatureMax]:0.0f}\u00b0F'
        u'/{daily_max_c}\u00b0C '
        u'Low: {daily[data][0][temperatureMin]:0.0f}\u00b0F'
        u'/{daily_min_c}\u00b0C ',
        u'',
        # u'{minutely[summary]} ',
        u'{hourly[summary]} ',
        u'{daily[summary]}'
    ]

    try:
        dt_current_time = datetime.utcfromtimestamp(args['currently']['time'])
        dt_current_time += timedelta(hours=args['offset'])
        current_time = dt_current_time.strftime('%Y/%m/%d %H:%M:%S')

        args.update(address=address)
        args.update(current_time=current_time)
        args.update(
            current_temperature_c=str(ftoc(args['currently']['temperature']))
        )
        args.update(
            feels_like_c=str(ftoc(args['currently']['apparentTemperature']))
        )
        args.update(
            daily_max_c=str(ftoc(args['daily']['data'][0]['temperatureMax']))
        )
        args.update(
            daily_min_c=str(ftoc(args['daily']['data'][0]['temperatureMin']))
        )
        args.update(
            humidity_pct=str(int(float(args['currently']['humidity']) * 100))
        )
        args.update(
            wind_kph=mphtokph(args['currently']['windSpeed'])
        )
        printthis = ""
        printthis += '\n'.join(template).format(**args)
    except:
        printthis = 'Not sure.'

    return printthis


def weather_get(input, token=None):
    address, result = weather_for_input(input, token=token)
    printthis = weather_print_result(address, result)
    return printthis
