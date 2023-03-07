from datetime import datetime, timedelta
from forecastio import load_forecast
from geopy.geocoders import Nominatim
from telegram import Update
from telegram.ext import ContextTypes


def f_to_c(x):
    return int((float(x) - 32.0) / 1.8)


def mph_to_kph(x):
    return x * 1.60934


def weather_for_input(text, token=None):
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
    print_this = ''
    if address is None or result is None:
        print_this += 'aroo?'
        return print_this
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


async def weather_get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = context.application.bot_data.get('config', {}).get('darksky_token')
    text = update.message.text
    text = text.removeprefix('/weather ')
    address, result = weather_for_input(text, token=token)
    try:
        print_this = weather_print_result(address, result)
    except BaseException as ex:
        print_this = 'not sure'
        print_this += " ({})".format(ex)
    await update.message.reply_text(print_this, reply_to_message_id=update.message.message_id)
