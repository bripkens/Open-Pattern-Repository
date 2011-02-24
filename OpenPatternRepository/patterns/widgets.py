#/usr/bin/env python2.6
# Copyright 2011 Ben Ripkens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__authors__ = [
        '"Ben Ripkens" <bripkens.dev@gmail.com>',
]

from itertools import chain
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django import forms

CHILD_START = True
CHILD_END = False

class TreeCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []

        has_id = attrs and 'id' in attrs

        final_attrs = self.build_attrs(attrs, name=name)

        output = ['<ul>']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])

        nodes = []

        for node in self.choices:
            self.generate_category_list(node, nodes)

        for i, node in enumerate(nodes):
            if node == CHILD_START:
                output.append('<ul>')
                continue
            elif node == CHILD_END:
                output.append('</ul>')
                continue
            elif i != 0:
                output.append('</li>')

            option_label = node.__unicode__()
            option_value = node.pk
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = ' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value
                                                                    : value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(node))
            output.append('<li><label%s>%s %s</label>' % (
            label_for, rendered_cb, option_label))

        output.append('</ul>')
        return mark_safe('\n'.join(output))

    def generate_category_list(self, node, list):
        list.append(node)

        if node.children.all():
            list.append(CHILD_START)

        for child_node in node.children.all():
            self.generate_category_list(child_node, list)

        if node.children.all():
            list.append(CHILD_END)