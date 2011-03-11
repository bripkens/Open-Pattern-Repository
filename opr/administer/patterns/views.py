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
from models.models import *
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
            p = save_new_pattern(mainForm, driverForm, relationshipForm,
                             templateRelatedForm)
            return HttpResponseRedirect(p.get_absolute_url())

    else:
        mainForm = ManagePatternForm()
        driverForm = DriverFormSet(prefix='driver')
        relationshipForm = RelationshipFormSet(prefix='relationships')
        templateRelatedForm = TemplateRelatedForm()

    context = {
        'form': mainForm,
        'driverForm': driverForm,
        'relationshipForm': relationshipForm,
        'templateRelated': templateRelatedForm,
        'active' : 3
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

    return p

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
