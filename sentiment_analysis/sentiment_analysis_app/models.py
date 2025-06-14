# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BrandAggregates(models.Model):
    brand = models.OneToOneField('Brands', models.DO_NOTHING, primary_key=True)  # The composite primary key (brand_id, date) found, that is not supported. The first column is selected.
    date = models.DateField()
    positive_count = models.IntegerField(blank=True, null=True)
    neutral_count = models.IntegerField(blank=True, null=True)
    negative_count = models.IntegerField(blank=True, null=True)
    total_reach = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
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
        managed = False
        db_table = 'brand_platform_aggregates'
        unique_together = (('brand', 'platform', 'date'),)


class Brands(models.Model):
    name = models.TextField(unique=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brands'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class NamedEntities(models.Model):
    post = models.ForeignKey('Posts', models.DO_NOTHING, blank=True, null=True)
    entity_text = models.TextField(blank=True, null=True)
    entity_label = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'named_entities'


class Platforms(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'platforms'


class Posts(models.Model):
    brand = models.ForeignKey(Brands, models.DO_NOTHING, blank=True, null=True)
    platform = models.ForeignKey(Platforms, models.DO_NOTHING, blank=True, null=True)
    platform_0 = models.CharField(db_column='platform', max_length=50, blank=True, null=True)  # Field renamed because of name conflict.
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
        managed = False
        db_table = 'sentiment_results'


class TopHandles(models.Model):
    user_id = models.TextField(unique=True)
    followers_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'top_handles'
