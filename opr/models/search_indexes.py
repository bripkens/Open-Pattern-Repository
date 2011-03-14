#/usr/bin/env python2.6

__authors__ = [
        '"Ben Ripkens" <bripkens.dev@gmail.com>',
]

import datetime
from haystack.indexes import *
from haystack import site
from opr.models.models import *


class PatternIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr='name')
    wiki_name = CharField(model_attr='wiki_name')
    tags = CharField(model_attr='tags')

    def get_queryset(self):
        return Pattern.objects.all()


site.register(Pattern, PatternIndex)