from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponse
import json
import random

def placeholder_view (request, **params):
    resolved = resolve(request.path_info)

    params = dict([(key, value) for key, value in params.items() if value is not None])

    namespace = '%s:' % resolved.namespace if resolved.namespace else ''
    view = namespace + resolved.url_name
    placeholders = dict((key, ('%0.'+str(len(value or ''))+'X').lower() % random.randint(0,0xFFFFFF)) for key, value in (params or {}).items())
    pattern = reverse(view, kwargs=placeholders)

    for key, value in placeholders.items():
        pattern = pattern.replace(value, '{'+key+'}')

    data = {
        'path': request.path_info,
        'name': resolved.url_name,
        'namespace': resolved.namespace,
        'params': params or None,
        'placeholders': placeholders or None,
        'pattern': pattern,
    }

    content = """
    <title>{view}</title>
    <style>
        body {{ font-family: sans-serif; padding: 5em; max-width: 800px; margin: 0 auto; }}
        h1 {{ border-bottom: solid 1px; }}
        dl {{ border: solid 1px #999; background: #EEE; padding: 1em; }}
        dt {{ width: 6em; float: left; clear: left; text-align: right; font-weight: bold; }}
        dt:after {{ content: ":"; }}
        dd {{ margin-left: 7em; }}
    </style>
    <h1>{view}</h1>
    <h2><code>{pattern}</code></h2>
    """.format(**{
        'view': view,
        'pattern': pattern,
    })

    if params:
        content += '<dl>\n%s\n</dl>' % (
            '\n'.join(['<dt>%s</dt><dd>%s</dd>' % (
                key, value
            ) for key, value in params.items()])
        )
            
    return HttpResponse(content)
