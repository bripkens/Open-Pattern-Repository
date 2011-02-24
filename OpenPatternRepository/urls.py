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

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
   (r'^', include('OpenPatternRepository.patterns.urls')),
   (r'^api/(?P<emitter_format>[a-zA-Z]+)/', include('OpenPatternRepository.api.urls')),
   (r'^admin/doc/', include('django.contrib.admindocs.urls')),
   (r'^admin/', include(admin.site.urls)),)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {
           'document_root': settings.STATIC_RESOURCE_FOLDER
        }),
    )