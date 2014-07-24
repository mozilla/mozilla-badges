from django.db.models import Field

def public_attributes (*args, **kwargs):
    attributes = dict([(key, kwargs.get(key, key)) for key in (list(args) + kwargs.keys())])

    def decorator (cls):
        cls.__public__ = attributes

        return cls

    return decorator
