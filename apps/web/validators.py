import re

from django.core.exceptions import ValidationError
from jinja2 import Environment, TemplateSyntaxError

from apps.web.utils import jinja2_extensions


def jinja2_template(value):
    try:
        env = Environment(extensions=jinja2_extensions())
        env.from_string(value)
    except TemplateSyntaxError:
        raise ValidationError(_("Jinja error: %(error)s"),
                              params={'error': value})


def validate_token(value):
    if not re.match('[0-9]+:[-_a-zA-Z0-9]+', value):
        raise ValidationError(
            _("%{value}s is not a valid token"),
            code='invalid',
            params={'value': value},
        )


def only_initial(value):
    from apps.web.models.step import Step
    if value and Step.objects.filter(is_initial=True).count():
        raise ValidationError(
            'Only one field must be unique',
            code='invalid',
        )


def username_list(value: str):
    for username in value.split(' '):
        if not re.match('[_a-zA-Z0-9]+', username):
            raise ValidationError(
                _("Username %(username)s is invalid"),
                code='invalid',
                params={'username': username},
            )
