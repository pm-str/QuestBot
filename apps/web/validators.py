import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from jinja2 import Environment, TemplateSyntaxError

from apps.web.conditions_parsing import NumericStringParser


def jinja2_template_validator(value: str):
    try:
        env = Environment(extensions=settings.JINJA2_EXTENTIONS)
        env.from_string(value)
    except TemplateSyntaxError:
        raise ValidationError(_("Jinja error: %(error)s"),
                              params={'error': value})


def token_validator(value: str):
    if not re.match('[0-9]+:[-_a-zA-Z0-9]+', value):
        raise ValidationError(
            _("%{value}s is not a valid token"),
            code='invalid',
            params={'value': value},
        )


def json_field_validator(value: str):
    return value


def initial_step_validator(value: str):
    from apps.web.models.step import Step
    if value and Step.objects.filter(is_initial=True).count():
        raise ValidationError(
            'Only one field must be unique',
            code='invalid',
        )


def username_list_validator(value: str):
    for username in value.split(' '):
        if not re.match('[_a-zA-Z0-9]+', username):
            raise ValidationError(
                _("Username %(username)s is invalid"),
                code='invalid',
                params={'username': username},
            )


def condition_validator(value: str):
    if re.match('^({\d*}\s*[*+!()]\s*)*{\d*}\s*$', value):
        return

    ex = value

    nsp = NumericStringParser()
    result = re.sub('{\d*}', '1', ex)
    try:
        nsp.eval(result)
    except BaseException as ex:
        raise ValidationError(
            _("Expression %(ids_expression)s is invalid"),
            code='invalid',
            params={'ids_expression': value},
        )
