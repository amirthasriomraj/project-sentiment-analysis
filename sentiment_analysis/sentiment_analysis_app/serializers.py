from rest_framework import serializers
from .models import *

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = '__all__'

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platforms
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'

class SentimentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentResults
        fields = '__all__'

class NamedEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = NamedEntities
        fields = '__all__'

class BrandAggregateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandAggregates
        fields = '__all__'

class BrandPlatformAggregateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandPlatformAggregates
        fields = '__all__'

class TopHandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopHandles
        fields = '__all__'
