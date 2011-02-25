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

from django.db import models
from tagging.models import Tag
from tagging.fields import TagField

class RelationshipType(models.Model):
    """A description for a relationship

    RelationshipType provides some meta information about the relationship.

    E.g. alternative, variant, depends on

    """

    name = models.CharField(max_length=100)

    # Optional description
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Category(models.Model):
    """Model for a category

    Categories can be used to categorize patterns

    """

    name = models.CharField(max_length=100)

    # Categories can have a parent category
    # blank and null are set to True to make this foreign key optional
    # TODO: Don't allow self references
    parent_category = models.ForeignKey('self', blank=True, null=True,
                                        related_name='children')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('view_category', [str(self.id)])

    class Meta:
        verbose_name_plural = 'Categories'

class License(models.Model):
    """License model

    A license can be attached to pattern descriptions.

    """

    name = models.CharField(max_length=100)

    restrictive = models.BooleanField(default=False)

    license_source = models.URLField(max_length=255)

    def __unicode__(self):
        return self.name

class QualityAttribute(models.Model):
    """Patterns can be rated according to these quality attributes

    """

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

DRIVER_CHOICES = (
('f', 'Force'),
('c', 'Consequence')
)

IMPACT_CHOICES = zip(range(1, 11),
                     ("1 (weak impact)", 2, 3, 4, 5, 6, 7, 8, 9,
                      "10 (strong impact)"))

class Driver(models.Model):
    """A driver can either be a consequence or a force

    """

    description = models.TextField(blank=True)

    type = models.CharField(max_length=1, choices=DRIVER_CHOICES)

    quality_attribute = models.ForeignKey(QualityAttribute)

    impact = models.IntegerField(default=5, choices=IMPACT_CHOICES)

    pattern = models.ForeignKey('PatternVersion', related_name='drivers')

    def __unicode__(self):
        return ''.join((self.quality_attribute.name,
                        ' [', str(self.impact), ']'))

    class Meta:
        unique_together = ('type', 'quality_attribute', 'pattern')

class Template(models.Model):
    """A template can be used for the documentation of a pattern

    """

    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True)

    author = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Component(models.Model):
    """A component is part of a template

    A textual element

    """

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    mandatory = models.BooleanField(default=False)

    sort_order = models.IntegerField(default=0)

    template = models.ForeignKey(Template, related_name='components')

    def __unicode__(self):
        return ''.join((self.template.name, ': ', self.name))

class TextBlock(models.Model):
    """TextBlock is the content specific to a pattern for a component
    
    """

    component = models.ForeignKey(Component)

    pattern = models.ForeignKey('PatternVersion', related_name='description')

    text = models.TextField(blank=True)

class Pattern(models.Model):
    """Pattern is a generic description for a solution...

    """

    name = models.CharField(max_length=100, unique=True)

    wiki_name = models.SlugField(max_length=100, unique=True)

    categories = models.ManyToManyField(Category, related_name='patterns',
                                        blank=True, null=True)

    tags = TagField()

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    @models.permalink
    def get_absolute_url(self):
        return ('view_pattern', None, {
            'name': self.name})

    def __unicode__(self):
        return self.name

class PatternVersion(models.Model):
    """A version of a specific pattern

    """

    pattern = models.ForeignKey(Pattern, related_name='versions')

    source = models.URLField(max_length=255, blank=True)

    author = models.CharField(max_length=255)

    documented_when = models.DateTimeField(auto_now=True)

    license = models.ForeignKey(License)

    template = models.ForeignKey(Template)

    def __unicode__(self):
        return ''.join(
                (self.pattern.name, '; Version: ', self.documented_when))

class Relationship(models.Model):
    """A relationship between two patterns

    """

    source = models.ForeignKey(Pattern, related_name='outgoing_relationships')

    target = models.ForeignKey(Pattern, related_name='incoming_relationships')

    type = models.ForeignKey(RelationshipType)

    description = models.TextField(blank=True)

    def __unicode__(self):
        return ''.join((self.source.name, ' <<', self.type.name, '>> ',
                        self.target.name))

    class Meta:
        unique_together = ('source', 'target', 'type')