import re

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from jinja2 import Environment, TemplateSyntaxError

from apps.web.conditions_parsing import NumericStringParser
from apps.web.utils import jinja2_extensions


def jinja2_template(value: str):
    try:
        env = Environment(extensions=jinja2_extensions())
        env.from_string(value)
    except TemplateSyntaxError:
        raise ValidationError(_("Jinja error: %(error)s"),
                              params={'error': value})


def validate_token(value: str):
    if not re.match('[0-9]+:[-_a-zA-Z0-9]+', value):
        raise ValidationError(
            _("%{value}s is not a valid token"),
            code='invalid',
            params={'value': value},
        )


def only_initial(value: str):
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


def validate_conditions(value: str):
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
