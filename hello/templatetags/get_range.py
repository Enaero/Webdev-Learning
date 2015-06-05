from django.template import Library

register = Library()
register.filter('get_range', get_range)

def get_range(n):
    return xrange(1, n+1)
