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
