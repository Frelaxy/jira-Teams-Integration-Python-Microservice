import datetime
import pytz


def convert_date_in_utc(date_string):
    date_object = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")
    date_object_with_utc = date_object.astimezone(pytz.timezone('Europe/Minsk'))
    updating_time = datetime.datetime.strftime(date_object_with_utc, "%d/%m/%Y %H:%M:%S")
    return updating_time


def try_or(string):
    try:
        return delete_incorrect_symbols(xstr(string))
    except (TypeError, KeyError, IndexError) as error:
        return ""


def xstr(value):
    xstr = lambda s: s or ""
    return xstr(value)


def delete_incorrect_symbols(string):
    symbols = {
        "\r\n\r\n": "\r\n",
        "\n\n": "\n",
        "\"": "",
        "\'": "",
        "\\": ""
    }
    for i, j in symbols.items():
        string = string.replace(i, j)
    return string
