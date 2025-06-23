# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BrandAggregates(models.Model):
    brand = models.OneToOneField('Brands', models.DO_NOTHING, primary_key=True)  # The composite primary key (brand_id, date) found, that is not supported. The first column is selected.
    date = models.DateField()
    positive_count = models.IntegerField(blank=True, null=True)
    neutral_count = models.IntegerField(blank=True, null=True)
    negative_count = models.IntegerField(blank=True, null=True)
    total_reach = models.BigIntegerField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'brand_aggregates'
        unique_together = (('brand', 'date'),)


class BrandPlatformAggregates(models.Model):
    brand = models.OneToOneField('Brands', models.DO_NOTHING, primary_key=True)  # The composite primary key (brand_id, platform, date) found, that is not supported. The first column is selected.
    platform = models.CharField(max_length=50)
    date = models.DateField()
    positive_count = models.IntegerField(blank=True, null=True)
    neutral_count = models.IntegerField(blank=True, null=True)
    negative_count = models.IntegerField(blank=True, null=True)
    total_reach = models.BigIntegerField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'brand_platform_aggregates'
        unique_together = (('brand', 'platform', 'date'),)


class Brands(models.Model):
    name = models.TextField(unique=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'brands'


class NamedEntities(models.Model):
    post = models.ForeignKey('Posts', models.DO_NOTHING, blank=True, null=True)
    entity_text = models.TextField(blank=True, null=True)
    entity_label = models.TextField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'named_entities'


class Platforms(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        #managed = False
        db_table = 'platforms'


# class Posts(models.Model):
#     brand = models.ForeignKey(Brands, models.DO_NOTHING, blank=True, null=True)
#     platform = models.ForeignKey(Platforms, models.DO_NOTHING, blank=True, null=True)
#     platform_0 = models.CharField(db_column='platform', max_length=50, blank=True, null=True)  # Field renamed because of name conflict.
#     raw_text = models.TextField()
#     cleaned_text = models.TextField()
#     user_id = models.TextField(blank=True, null=True)
#     original_post_url = models.TextField(blank=True, null=True)
#     posted_at = models.DateTimeField(blank=True, null=True)
#     language = models.CharField(max_length=50, blank=True, null=True)
#     reach_estimate = models.BigIntegerField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     like_count = models.IntegerField(blank=True, null=True)
#     view_count = models.IntegerField(blank=True, null=True)
#     share_count = models.IntegerField(blank=True, null=True)
#     comment_count = models.IntegerField(blank=True, null=True)
#     followers_count = models.IntegerField(blank=True, null=True)
#     state = models.CharField(max_length=50, blank=True, null=True)
#     country = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         #managed = False
#         db_table = 'posts'


class Posts(models.Model):
    brand = models.ForeignKey('Brands', models.DO_NOTHING, db_column='brand_id', blank=True, null=True)
    platform = models.ForeignKey('Platforms', models.DO_NOTHING, db_column='platform_id', blank=True, null=True)
    #platform_text = models.CharField(db_column='platform', max_length=50, blank=True, null=True)
    raw_text = models.TextField()
    cleaned_text = models.TextField()
    user_id = models.TextField(blank=True, null=True)
    original_post_url = models.TextField(blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    reach_estimate = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    like_count = models.IntegerField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    share_count = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    followers_count = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'


class SentimentResults(models.Model):
    post = models.ForeignKey(Posts, models.DO_NOTHING, related_name='sentiment', blank=True, null=True)
    sentiment_label = models.TextField(blank=True, null=True)
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'sentiment_results'


class TopHandles(models.Model):
    user_id = models.TextField(unique=True)
    followers_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'top_handles'
