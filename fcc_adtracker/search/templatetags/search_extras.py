from django import template

register = template.Library()


def spliton(value, arg):
    return value.split(arg)

register.filter('spliton', spliton)


def replace(value, arg):
    ''' Takes comma-separated values in the argument.
        The first value is the character to replace,
        the second is what will be put in its place
    '''
    (old, new) = arg.split(',')
    return value.replace(old, new)

register.filter('replace', replace)
