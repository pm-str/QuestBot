import ast

from constance import config
from django.conf import settings


def plain_to(value, instance=list):
    if isinstance(value, instance):
        for i in value:
            for item in plain_to(i, instance):
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


def clear_redundant_tags(text: str) -> str:
    cp = text

    tags_mapping = {
        '<br />': '',
    }

    for (key, value) in tags_mapping.items():
        cp = cp.replace(key, value)

    return cp
