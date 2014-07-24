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
