import datetime

from mozbadges.compat import json


class LazyEncoder(json.JSONEncoder):
    """
    JSONEncoder that turns Promises into unicode strings to support functions
    like ugettext_lazy and reverse_lazy.
    """
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


def time_since(otherdate=None, offset=None, now=None, fuzzy=True, format='%A, %Y %B %m, %H:%I'):
    def humanize(*numbers):
        words = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
        return tuple([words[number] if number <= 10 else number for number in numbers])

    def pluralize(*numbers):
        data = [(number, '' if number == 1 else 's') for number in numbers]
        print numbers, data, [item for sublist in data for item in sublist]
        return tuple([item for sublist in data for item in sublist])

    if now is None:
        now = datetime.datetime.now()

    if otherdate:
        td = now - otherdate
        offset = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

    if offset:
        delta_s = offset % 60
        offset /= 60
        delta_m = offset % 60
        offset /= 60
        delta_h = offset % 24
        offset /= 24
        delta_d = offset
    else:
        raise ValueError("Must supply otherdate or offset (from now)")

    if delta_d > 1:
        if delta_d > 6:
            date = now + datetime.timedelta(days=-delta_d, hours=-delta_h, minutes=-delta_m)
            return date.strftime(format)
        else:
            wday = now + datetime.timedelta(days=-delta_d)
            return wday.strftime('%A')

    if delta_d == 1:
        return "Yesterday"

    if delta_h > 0:
        if fuzzy:
            if delta_m >= 30:
                delta_h += 1
            return "%s hours ago" % pluralize(*humanize(delta_h))
        else:
            return "%s hour%s %s minute%s ago" % pluralize(delta_h, delta_m)

    if delta_m > 0:
        if fuzzy:
            if delta_m >= 45:
                return '1 hour ago'

            if delta_m >= 25:
                return 'half an hour ago'

            if delta_s >= 30:
                delta_m += 1
            return "%s minute%s ago" % pluralize(*humanize(delta_m))
        else:
            return "%s minute%s %s second%s ago" % pluralize(delta_m, delta_s)

    if fuzzy:
        return "just now"
    else:
        return "%s second%s ago" % pluralize(delta_s)
