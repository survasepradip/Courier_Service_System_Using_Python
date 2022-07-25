from textwrap import wrap
from django.core.exceptions import PermissionDenied

def is_admin(function):
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='company_admin').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def is_depot_admin(function):
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='depot_admin').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap