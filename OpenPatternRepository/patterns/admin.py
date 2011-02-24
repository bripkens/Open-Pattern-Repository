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

from django.contrib import admin
from models import *


class RelationshipTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ('name', 'description')

admin.site.register(RelationshipType, RelationshipTypeAdmin)


class CategoryAdmin(admin.ModelAdmin):
    search_fields =  ('name',)

    list_display = ('name', 'parent_category')

admin.site.register(Category, CategoryAdmin)


class LicenseAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    list_display = ('name', 'restrictive')

    list_filter = ('restrictive',)

admin.site.register(License, LicenseAdmin)


class QualityAttributeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')

    list_display = ('name',)

admin.site.register(QualityAttribute, QualityAttributeAdmin)

class ComponentInline(admin.TabularInline):
    model = Component
    extra = 3

class TemplateAdmin(admin.ModelAdmin):
    inlines = (ComponentInline,)

    list_display = ('name', 'author')

    search_fields = ('name', 'description', 'author')

admin.site.register(Template, TemplateAdmin)