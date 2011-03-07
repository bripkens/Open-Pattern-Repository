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

from opr.models.models import *
from tagging.models import Tag, TaggedItem
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

def browse_categories(request, categoryName=None):
    """Provide a category view for a categories or just a specific one

    """
    # TODO when the system is growing it would be more appropriate to serve
    # only parts of the hierarchy (performance reasons)

    if not categoryName == None:
        try:
            allCategories = Category.objects.get(name__iexact=categoryName)
            allCategories = [allCategories]
        except Category.DoesNotExist:
            allCategories = None

    if allCategories == None:
        allCategories = Category.objects.filter(parent_category=None).order_by(
                'name').all()

    result = []

    for category in allCategories:
        add_category(category, result)

    result.extend(Pattern.objects.filter(categories=None))

    return render_to_response('patterns/browse_patterns.html', {
        'data': result
        })

def add_category(category, list):
    """Recursive method that is used to generate a hierachiral category list

    """

    list.append(category)

    child_categories = category.children.order_by('name').all()
    patterns = category.patterns.order_by('name').all()

    if len(child_categories) > 0 or len(patterns) > 0:
        # category names are trimmed. Therefore using whitespace as the first
        # and last character is save for distinction between marker and entry
        list.append(' sub start ')

    for child_category in child_categories:
        add_category(child_category, list)

    for pattern in patterns:
        list.append(pattern)

    if len(child_categories) > 0 or len(patterns) > 0:
        list.append(' sub end ')

    list.append(' row end ')

def view_pattern(request, wiki_name):
    """View details for a given pattern.

    TODO what about a generic view for this?
    A generic view may not be appropriate as the newest version needs to be
    determined

    """
    pattern = get_object_or_404(Pattern, wiki_name__iexact=wiki_name)
    version = pattern.get_current_version()
    return HttpResponse(version)

def with_tag(request, tag):
    """Retrieve a list of patterns that have the given tag.

    """
    query_tag = Tag.objects.get(name=tag)
    entries = TaggedItem.objects.get_by_model(Pattern, query_tag)
    entries = entries.order_by('name')

    return render_to_response("patterns/with_tag.html", {
        'tag' : tag,
        'entries' : entries
    })