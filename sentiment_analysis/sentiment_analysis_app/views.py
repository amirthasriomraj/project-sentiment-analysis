from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.core.paginator import Paginator
from django.db.models import Q

from .models import *
from .serializers import *
from .filters import *


def home(request):
    query = request.GET.get('q', '')
    brand = request.GET.get('brand', '')
    platform = request.GET.get('platform', '')
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    posts = Posts.objects.select_related('brand', 'platform').all()

    # Apply filters
    if query:
        posts = posts.filter(cleaned_text__icontains=query)

    if brand:
        posts = posts.filter(brand__name=brand)

    if platform:
        posts = posts.filter(platform__name=platform)

    if from_date:
        posts = posts.filter(created_at__date__gte=from_date)
    if to_date:
        posts = posts.filter(created_at__date__lte=to_date)

    posts = posts.order_by('-created_at')

    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    results = []
    for post in page_obj:
        sentiment = SentimentResults.objects.filter(post=post).first()
        results.append({
            'post': post,
            'sentiment_label': sentiment.sentiment_label if sentiment else 'N/A',
            'sentiment_score': sentiment.sentiment_score if sentiment else '-',
        })

    context = {
        'results': results,
        'page_obj': page_obj,
        'brands': Brands.objects.values_list('name', flat=True).distinct(),
        'platforms': Platforms.objects.values_list('name', flat=True).distinct(),
        'query': query,
        'selected_brand': brand,
        'selected_platform': platform,
        'from_date': from_date,
        'to_date': to_date,
    }

    return render(request, 'home.html', context)


# REST API ViewSets (unchanged)
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
