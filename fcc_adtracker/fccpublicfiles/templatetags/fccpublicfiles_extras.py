from django import template

register = template.Library()

DAY_CHOICES = (
    (0, "Monday", u'Mon', u'M'),
    (1, "Tuesday", u'Tue', u'T'),
    (2, "Wednesday", u'Wed', u'W'),
    (3, "Thursday", u'Thu', u'R'),
    (4, "Friday", u'Fri', u'F'),
    (5, "Saturday", u'Sat', u'Sa'),
    (6, "Sunday", u'Sun', u'Su')
)

def weekday_int_formatter(value, arg=None):
    """ Formats a single integer or list of weekday integers according to a given format.
        Accepts the following 'Day of Week' format strings (based on date string format synax):
            'l'  Day of the week, textual, long.
            'D'  Day of the week, textual, 3 letters.
            'D1' Day of the week from M,T,W,R,F,Sa,Su
            'w'  Day of the week, digits (yes, same as input)
        Returns a string or list of strings.
    """
    format_code = arg if arg in ('l', 'D', 'D1', 'w') else 'w'
    output = value
    if format_code == 'D':
        format_pos = 2
    elif format_code == 'D1':
        format_pos = 3
    elif format_code == 'w':
        format_pos = 0
    else:
        format_pos = 1

    if isinstance(value, list):
        output = [DAY_CHOICES[x][format_pos] for x in value]
    elif isinstance(value, int):
        if 0 <= value < 6:
            output = u'{0}'.format(DAY_CHOICES[value][format_pos])

    return output


register.filter('weekday', weekday_int_formatter)