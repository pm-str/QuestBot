import ast

from constance import config
from django.conf import settings


def traverse(value, instance=list):
    if isinstance(value, instance):
        for i in value:
            for item in traverse(i, instance):
                yield item
    else:
        yield value


def jinja2_extensions():
    extensions = getattr(config, settings.JINJA2_EXTENTIONS, [])
    try:
        return ast.literal_eval(extensions)
    except ValueError:
        return []


def jinja2_template_context():
    extensions = getattr(config, settings.JINJA2_TEMPLATES_CONTEXT, {})
    try:
        value = ast.literal_eval(extensions)
        assert isinstance(value, dict)
    except ValueError:
        value = {}

    return value
