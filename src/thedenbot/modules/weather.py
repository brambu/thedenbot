""" /weather command """
from datetime import datetime, timedelta
from logging import getLogger
from forecastio import load_forecast
from geopy.geocoders import Nominatim
from telegram import Update
from telegram.ext import ContextTypes

log = getLogger(__name__)


def f_to_c(f_temp):
    """ convert temp unit """
    return int((float(f_temp) - 32.0) / 1.8)


def mph_to_kph(mph):
    """ convert speed unit """
    return mph * 1.60934


def weather_for_input(text, token=None):
    """ get weather for input like 'San Jose' """
    geolocator = Nominatim(user_agent='brambu/thedenbot/modules/weather')
    location = geolocator.geocode(text)
    if location is None:
        return None, None
    ret = load_forecast(token,
                        location.latitude,
                        location.longitude,
                        units='us')
    result = ret.json
    return location.address, result


def weather_print_result(address, result):
    """ print a forecastio forecast result """
    print_this = ''
    if address is None or result is None:
        print_this += 'aroo?'
        return print_this
    args = {}
    args.update(**result)
    args.update(address=address)
    template = [
        'Weather for {address}',
        '{current_time} {timezone}',
        '',
        'Currently: {currently[summary]} '
        '{currently[temperature]:0.0f}\u00b0F/{current_temperature_c}\u00b0C '
        'Feels like: {currently[apparentTemperature]:0.0f}\u00b0F'
        '/{feels_like_c}\u00b0C',
        'humidity: {humidity_pct}%, wind: {currently[windSpeed]}mph'
        '/{wind_kph:.2f}kph',
        'High: {daily[data][0][temperatureMax]:0.0f}\u00b0F'
        '/{daily_max_c}\u00b0C '
        'Low: {daily[data][0][temperatureMin]:0.0f}\u00b0F'
        '/{daily_min_c}\u00b0C ',
        '',
        # '{minutely[summary]} ',
        '{hourly[summary]} ',
        '{daily[summary]}'
    ]
    dt_current_time = datetime.utcfromtimestamp(args['currently']['time'])
    dt_current_time += timedelta(hours=args['offset'])
    current_time = dt_current_time.strftime('%Y/%m/%d %H:%M:%S')
    args.update(address=address)
    args.update(current_time=current_time)
    args.update(
        current_temperature_c=str(f_to_c(args['currently']['temperature']))
    )
    args.update(
        feels_like_c=str(f_to_c(args['currently']['apparentTemperature']))
    )
    args.update(
        daily_max_c=str(f_to_c(args['daily']['data'][0]['temperatureMax']))
    )
    args.update(
        daily_min_c=str(f_to_c(args['daily']['data'][0]['temperatureMin']))
    )
    args.update(
        humidity_pct=str(int(float(args['currently']['humidity']) * 100))
    )
    args.update(
        wind_kph=mph_to_kph(args['currently']['windSpeed'])
    )
    print_this += '\n'.join(template).format(**args)
    return print_this


async def weather_get(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """ example /weather San Jose """
    token = context.application.bot_data.get('config', {}).get('darksky_token')
    text = update.message.text
    text = text.removeprefix('/weather ')
    address, result = weather_for_input(text, token=token)
    try:
        print_this = weather_print_result(address, result)
    except BaseException as ex:
        print_this = 'not sure'
        log.warning('weather error %s', ex)
    await update.message.reply_text(
        print_this,
        reply_to_message_id=update.message.message_id,
    )
