from django.http import HttpResponse
from django.shortcuts import render


def public_attributes (*args, **kwargs):
    attributes = dict([(key, kwargs.get(key, key)) for key in (list(args) + kwargs.keys())])

    def decorator (cls):
        cls.__public__ = attributes

        return cls

    return decorator


def render_to(template_name):
    def decorator(fn):
        def view(request, *args, **kwargs):
            response = fn(request, *args, **kwargs)

            if response is None:
                response = {}

            if not isinstance(response, dict):
                return response

            return render(request, template_name, response)
        return view
    return decorator


def requires_user(fn=None, *attrs):
    attrs += ('is_authenticated',)
    def decorator(fn):
        def view(request, *args, **kwargs):
            user = request.user
            valid = True
            for attr in attrs:
                value = valid and getattr(user, attr, False)
                if callable(value):
                    value = value()
                valid = valid and value

            if valid:
                return fn(request, *args, **kwargs)

            return render(request, '401.html', {})
        return view
    if callable(fn):
        return decorator(fn)
    else:
        attrs = (fn,) + attrs
    return decorator