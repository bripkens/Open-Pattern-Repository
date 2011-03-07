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

from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import fields_for_model
from models.models import *
from administer.patterns.widgets import TreeCheckboxSelectMultiple

# activate ajax validation
# TODO find a better place for this, e.g. external app
from ajaxvalidation.fields import activate_javascript_validation_mandatories
activate_javascript_validation_mandatories()

class DynForm(forms.Form):
    def __init__(self, *args, **kwargs):
        extra_fields = None

        if 'fields' in kwargs:
            extra_fields = kwargs.pop('fields')

        if not extra_fields:
            extra_fields = {}

        super(DynForm, self).__init__(*args, **kwargs)

        for name, field in extra_fields.items():
            self.fields[name] = field

class TemplateRelatedForm(DynForm):
    def __init__(self, *args, **kwargs):
        fields = {}

        if 'template' in kwargs:
            template = kwargs.pop('template')
            if template:
                for component in template.components.all():
                    field = forms.CharField(label=component.name,
                                            help_text=component.description,
                                            required=component.mandatory,
                                            widget=forms.Textarea(attrs={
                                                'rows': 15,
                                                'cols': 75
                                                }))
                    fields["description-" + str(component.id)] = field

        kwargs['fields'] = fields
        super(TemplateRelatedForm, self).__init__(*args, **kwargs)

class ManagePatternForm(forms.Form):
# May be useful later on
# http://stackoverflow.com/questions/2196797/django-input-element-error-css-class
# http://docs.djangoproject.com/en/dev/ref/forms/api/#styling-required-or-erroneous-form-rows
#required_css_class = "required"
#error_css_class = "error"

#    class MyForm(forms.Form):
#    """
#    Extend from this form so your widgets have an 'error' class if there's
#    an error on the field.
#    """
#    def __init__(self, *args, **kwargs):
#        super(MyForm, self).__init__(*args, **kwargs)
#        if self.errors:
#            for f_name in self.fields:
#                if f_name in self.errors:
#                    classes = self.fields[f_name].widget.attrs.get('class', '')
#                    classes += ' errors'
#                    self.fields[f_name].widget.attrs['class'] = classes

    def __init__(self, *args, **kwargs):
        super(ManagePatternForm, self).__init__(*args, **kwargs)
        root_categories = Category.objects.filter(parent_category=None)
        self.fields['categories'].choices = root_categories

    _pattern_fields = fields_for_model(Pattern)
    name = _pattern_fields['name']
    name.widget.attrs.update({'autofocus': 'autofocus'})

    permalink = _pattern_fields['wiki_name']
    categories = _pattern_fields['categories']
    categories.widget = TreeCheckboxSelectMultiple()

    tags = _pattern_fields['tags']

    _pattern_version_fields = fields_for_model(PatternVersion)
    author = _pattern_version_fields['author']
    source = _pattern_version_fields['source']
    license = _pattern_version_fields['license']
    template = _pattern_version_fields['template']

    def clean_name(self):
        name = self.cleaned_data['name']
        print name
        try:
            Pattern.objects.get(name__iexact=name)
            raise forms.ValidationError("This name is already used.")
        except Pattern.DoesNotExist:
            return name

    def clean_permalink(self):
        permalink = self.cleaned_data['permalink']

        try:
            Pattern.objects.get(wiki_name=permalink)
            raise forms.ValidationError("This permalink is already used.")
        except Pattern.DoesNotExist:
            return permalink


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('quality_attribute', 'impact', 'type', 'description')

DriverFormSet = formset_factory(DriverForm)

class RelationshipForm(forms.ModelForm):
    class Meta:
        model = Relationship
        fields = ('target', 'type', 'description')

RelationshipFormSet = formset_factory(RelationshipForm)