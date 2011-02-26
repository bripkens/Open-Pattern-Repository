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

from forms import ManagePatternForm
from forms import DriverFormSet
from forms import RelationshipFormSet
from forms import TemplateRelatedForm
from models import *
from tagging.models import Tag, TaggedItem
from django.core.context_processors import csrf
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

def add_pattern(request):
    """Add a pattern view.

    """
    if request.method == 'POST':
        mainForm = ManagePatternForm(request.POST)
        driverForm = DriverFormSet(request.POST, request.FILES,
                                   prefix='driver')
        relationshipForm = RelationshipFormSet(request.POST, request.FILES,
                                               prefix='relationships')
        template = get_template(request, mainForm)
        templateRelatedForm = TemplateRelatedForm(request.POST,
                                                  template=template)

        if (mainForm.is_valid() and driverForm.is_valid() and
            relationshipForm.is_valid() and templateRelatedForm.is_valid()):
            save_new_pattern(mainForm, driverForm, relationshipForm,
                             templateRelatedForm)
            return HttpResponseRedirect('/pattern/name')

    else:
        mainForm = ManagePatternForm()
        driverForm = DriverFormSet(prefix='driver')
        relationshipForm = RelationshipFormSet(prefix='relationships')
        templateRelatedForm = TemplateRelatedForm()

    context = {
        'form': mainForm,
        'driverForm': driverForm,
        'relationshipForm': relationshipForm,
        'templateRelated': templateRelatedForm
    }
    context.update(csrf(request))

    return render_to_response('patterns/manage_pattern.html', context)

def get_template(request, mainForm):
    """Utility function that will try to return the template that is
    associated with the request.

    For performance resources the forms cleaned data template attribute
    will be used. When the request is invalid it will be tried to retrieve
    the template based on the requests post parameter.

    None is returned in case that no template could be retrieved from the
    request.

    """
    if mainForm.is_valid():
        template = mainForm.cleaned_data['template']
    else:
        try:
            template_param = request.POST['template']
        except MultiValueDictKeyError:
            return

        if not template_param:
            return

        try:
            template = Template.objects.get(pk=int(template_param))
        except Template.DoesNotExist:
            return

    return template

def save_new_pattern(mainForm, driverFormSet, relationshipFormSet,
                     templateRelatedForm):
    """Save a pattern to the database

    This function is only useful for the add pattern view and should not be
    used by any other view.

    """
    # TODO verify that everything is done in a single transaction
    p = Pattern()
    p.name = mainForm.cleaned_data['name']
    p.wiki_name = mainForm.cleaned_data['permalink']

    p.save()

    p.categories = mainForm.cleaned_data['categories']
    p.tags = mainForm.cleaned_data['tags']
    p.save()

    v = PatternVersion()
    v.license = mainForm.cleaned_data['license']
    v.author = mainForm.cleaned_data['author']
    v.source = mainForm.cleaned_data['source']
    v.template = mainForm.cleaned_data['template']
    v.pattern = p

    v.save()

    # textual description
    for component in v.template.components.all():
        block = TextBlock()
        block.component = component
        block.pattern = v
        block.text = templateRelatedForm.cleaned_data['description-' +
                                                      str(component.id)]

        block.save()

    # driver
    for driverForm in driverFormSet.cleaned_data:
        # a simple check that verifies that data has been entered into
        # this form. There should be another way to handle this case!
        # TODO find a better solution
        if not driverForm.get('quality_attribute') == None:
            driver = Driver()
            driver.pattern = v
            driver.impact = driverForm['impact']
            driver.quality_attribute = driverForm['quality_attribute']
            driver.type = driverForm['type']
            driver.description = driverForm['description']
            driver.save()

    # relationships
    for relationshipForm in relationshipFormSet.cleaned_data:
        # a simple check that verifies that data has been entered into
        # this form. There should be another way to handle this case!
        # TODO find a better solution
        if not relationshipForm.get('target') == None:
            relationship = Relationship()
            relationship.source = p
            relationship.target = relationshipForm['target']
            relationship.description = relationshipForm['description']
            relationship.type = relationshipForm['type']
            relationship.save()

def propose_tags(request, query=""):
    """Propose some tags to the user.

    Tags will be returned in json format. Minimum query length is 3.

    """
    query = query.strip()

    if len(query) < 3:
        return HttpResponseBadRequest('Minimum three characters.')

    # TODO use some full text search engine for this
    query_result = Tag.objects.filter(name__icontains=query)
    json = simplejson.dumps([tag.name for tag in query_result])
    return HttpResponse(json, 'application/json')

def preview_markdown(request):
    """Provide a request parameter called data which should be run through
    the markdown filter.

    The transformed input will be returned.

    """
    # TODO make sure that this service can't be exploited

    try:
        markdown = request.REQUEST['data']
    except KeyError:
        return HttpResponseBadRequest(
                'GET/POST with "data" parameter required.')

    # TODO actually there should be a simpler way. Investigate
    return render_to_response('patterns/markdown_preview.html', {
        'markdown': markdown
        })

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

    # we want to use the django unordered list filter hence we must adhere to
    # the required data structure
    result = []

    for category in allCategories:
        add_category(category, result)

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

def view_pattern(request, name):
    """View details for a given pattern.

    TODO what about a generic view for this?
    A generic view may not be appropriate as the newest version needs to be
    determined

    """
    pattern = get_object_or_404(Pattern, name__iexact=name)
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