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

from piston.handler import BaseHandler
from patterns.models import *
from django.shortcuts import _get_queryset


def get_object_or_none(klass, *args, **kwargs):
    """Utility function just list django.shortcuts.get_object_or_404

    Instead of raising a 404 error this function returns None.

    See: django.shortcuts.get_object_or_404

    """

    queryset = _get_queryset(klass)

    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None

class TemplateHandler(BaseHandler):
    """Retrieve the templates that are available.

    """

    allowed_methods = ('GET',)
    model = Template
    fields = ('id', 'name', 'description', 'author',
              ('components', ('id', 'name', 'description', 'mandatory',
                              'sort_order')))

    def read(self, request, id=None):
        """Retrieve one or more template

        If you call this method with the 'id' parameter then one entity will
        be returned or null if there is no entity for given id.

        Calling this method without the id parameter will result in
        all templates.

        """

        if id:
            return get_object_or_none(Template, pk=id)
        else:
            return Template.objects.all()

class PatternHandler(BaseHandler):
    """Retrieve all patterns or a single one

    """
    allowed_methods = ('GET',)
    model = Pattern
    fields = ('id', 'name', 'wiki_name', 'tags', 'categories', ('versions', (
    'source', 'author', 'documented_when', 'license', 'template',
    ('description', ('text', ('component', ('name', 'sort_order')))))))

    def read(self, request, id=None):
        """Retrieve one or more patterns

        If you call this method with the 'id' parameter then one entity will
        be returned or null if there is no entity for given id.

        Calling this method without the id parameter will result in
        all patterns.

        """

        if id:
            return get_object_or_none(Pattern, pk=id)
        else:
            return Pattern.objects.all()

class PatternVersionHandler(BaseHandler):
    """For now just a definition of the data that will be published

    """

    model = PatternVersion
    fields = ('source', 'author', 'documented_when', 'license', 'template')

class CategoryHandler(BaseHandler):
    """For now just a definition of the data that will be published

    """

    model = Category
    fields = ('id', 'name')

class LicenseHandler(BaseHandler):
    """For now just a definition of the data that will be published

    """

    model = License
    fields = ('id', 'license_source', 'restrictive')