import django_filters # type: ignore
from django.db import models

class BaseInsensitiveFilterSet(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filter_ in self.filters.items():
            field = self._meta.model._meta.get_field(name)
            if isinstance(field, (models.CharField, models.TextField)):
                # Override lookup expression
                filter_.lookup_expr = 'iexact'


from .models import *

class BrandFilter(BaseInsensitiveFilterSet):
    class Meta:
        model = Brands
        fields = ['name']

class PlatformFilter(BaseInsensitiveFilterSet):
    class Meta:
        model = Platforms
        fields = ['name']

class PostFilter(BaseInsensitiveFilterSet):
    class Meta:
        model = Posts
        fields = ['platform', 'user_id', 'created_at', 'brand']

class SentimentResultFilter(BaseInsensitiveFilterSet):
    class Meta:
        model = SentimentResults
        fields = ['post', 'sentiment_score', 'sentiment_label']

class NamedEntityFilter(BaseInsensitiveFilterSet):
    class Meta:
        model = NamedEntities
        fields = ['entity_text', 'entity_label', 'post']

class BrandAggregateFilter(BaseInsensitiveFilterSet):
    class Meta:
        model = BrandAggregates
        fields = ['brand', 'date']

class BrandPlatformAggregateFilter(BaseInsensitiveFilterSet):
    class Meta:
        model = BrandPlatformAggregates
        fields = ['brand', 'platform', 'date']

class TopHandleFilter(BaseInsensitiveFilterSet):
    class Meta:
        model = TopHandles
        fields = ['user_id', 'created_at']


