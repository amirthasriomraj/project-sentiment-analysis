from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'brands', views.BrandViewSet)
router.register(r'platforms', views.PlatformViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'sentiments', views.SentimentResultViewSet)
router.register(r'entities', views.NamedEntityViewSet)
router.register(r'brand-aggregates', views.BrandAggregateViewSet)
router.register(r'brand-platform-aggregates', views.BrandPlatformAggregateViewSet)
router.register(r'top-handles', views.TopHandleViewSet)


urlpatterns = [
    # Frontend homepage
    path('', views.home, name='home'),

    # API routes (mounted at /api/)
    path('api/', include(router.urls)),
]