#/usr/bin/env python2.6

__authors__ = [
        '"Ben Ripkens" <bripkens.dev@gmail.com>',
]

from django.forms.fields import *
from django.forms.forms import BoundField
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape


def prepare_error_for_html(error):
    return conditional_escape(force_unicode(error))

possible_ajax_validations = (
    # required
    (lambda self: self.field.required, 'required', 'val-required',
     lambda self, error_message: prepare_error_for_html(error_message)),
    # url
    (lambda self: isinstance(self.field, URLField), 'invalid', 'val-url',
    lambda self, error_message: prepare_error_for_html(error_message)),
)


original_boundfield_as_widget = BoundField.as_widget

def add_required_class(self, *args, **kwargs):
    html = original_boundfield_as_widget(self, args, kwargs)
    result = [html]

    field_errors = set(self.errors[:])

    result.append(u'<ul class="val-constraints">')

    for validation in possible_ajax_validations:
        if not validation[0](self):
            continue;
            
        msg = self.field.error_messages[validation[1]]

        show_error = False
        if msg in field_errors:
            show_error = True

        active = u'val-show' if show_error else u'val-hide'

        result.append(u'<li class="')
        result.append(validation[2])
        result.append(' ')
        result.append(active)
        result.append(u'">')
        result.append(validation[3](self, msg))
        result.append(u'</li>')

        if show_error:
            field_errors.remove(msg)

    for unhandled_error in field_errors:
        result.append(u'<li class="val-unhandled val-show">')
        result.append(unhandled_error)
        result.append(u'</li>')

    result.append(u'</ul>')

    return mark_safe(''.join(result))



def activate_javascript_validation_mandatories():
    BoundField.as_widget = add_required_class
