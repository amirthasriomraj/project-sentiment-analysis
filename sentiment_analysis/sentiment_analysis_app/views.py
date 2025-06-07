from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend # type: ignore

from .models import *
from .serializers import *
from .filters import *

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BrandFilter

class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platforms.objects.all()
    serializer_class = PlatformSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlatformFilter

class PostViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

class SentimentResultViewSet(viewsets.ModelViewSet):
    queryset = SentimentResults.objects.all()
    serializer_class = SentimentResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SentimentResultFilter

class NamedEntityViewSet(viewsets.ModelViewSet):
    queryset = NamedEntities.objects.all()
    serializer_class = NamedEntitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NamedEntityFilter

class BrandAggregateViewSet(viewsets.ModelViewSet):
    queryset = BrandAggregates.objects.all()
    serializer_class = BrandAggregateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BrandAggregateFilter

class BrandPlatformAggregateViewSet(viewsets.ModelViewSet):
    queryset = BrandPlatformAggregates.objects.all()
    serializer_class = BrandPlatformAggregateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BrandPlatformAggregateFilter

class TopHandleViewSet(viewsets.ModelViewSet):
    queryset = TopHandles.objects.all()
    serializer_class = TopHandleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TopHandleFilter
