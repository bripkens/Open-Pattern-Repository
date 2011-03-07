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
from administer.patterns.views import *

urlpatterns = patterns('administer.patterns.views',
                       (r'^pattern/add/$', 'add_pattern'),
                       (r'^suggest/tag/(?P<query>.+)$', propose_tags),
                       (r'^preview/markdown/', preview_markdown)
                       )