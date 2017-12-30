import ast

from django.conf import settings
from django.http import HttpResponse

from rest_framework import status

from constance import config


def plain_to(value, instance=list):
    if isinstance(value, instance):
        for i in value:
            for item in plain_to(i, instance):
                yield item
    else:
        yield value


def jinja2_template_context():
    extensions = getattr(config, settings.JINJA2_TEMPLATES_CONTEXT, {})
    try:
        value = ast.literal_eval(extensions)
        assert isinstance(value, dict)
    except ValueError:
        value = {}

    return value


def clear_redundant_tags(text: str) -> str:
    cp = text

    tags_mapping = {
        '<br />': '',
        '&nbsp;': ' ',
    }

    for (key, value) in tags_mapping.items():
        cp = cp.replace(key, value)

    return cp


def allowed_hooks(func):
    def wrapper(*args, **kwargs):
        request = args[1]
        data = request.data
        not_supported = [
            'edited_message',
        ]
        for flags in not_supported:
            if flags in data:
                # It would be better to specify HTTP_501_NOT_IMPLEMENTED,
                # but in this case the request will be repeats
                return HttpResponse(status=status.HTTP_204_NO_CONTENT)

        return func(*args, **kwargs)
    return wrapper
