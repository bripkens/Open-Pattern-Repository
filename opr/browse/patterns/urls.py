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

from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

urlpatterns = patterns('browse.patterns.views',
                       url(r'^browse/(?P<categoryName>.*)$', 'browse_categories',
                           name='browse_categories'),
                       (r'^tag/(?P<tag>[-_A-Za-z0-9]+)/$', 'with_tag'),
                       url(r'^patterns/(?P<wiki_name>.*)/$', 'view_pattern',
                           name='view_pattern')
                       )