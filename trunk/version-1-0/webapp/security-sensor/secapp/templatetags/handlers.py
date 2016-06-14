from django import template

register = template.Library()


def get_seconds_ts(timestamp):

    return timestamp.strftime("%S")


def get_miliseconds_ts(timestamp):

    return timestamp.strftime("%f")


register.filter(get_seconds_ts)
register.filter(get_miliseconds_ts)
