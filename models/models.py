
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import os

from django.conf import settings
from django.db import models


class Media(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_name = models.CharField(max_length=255)
    m_type = models.IntegerField()
    m_rate = models.FloatField(blank=True, null=True)
    m_rate_num = models.IntegerField(blank=True, null=True)
    m_heat = models.IntegerField(blank=True, null=True)
    m_profile_photo = models.ForeignKey('Picture', models.DO_NOTHING, db_column='m_profile_photo', blank=True, null=True)
    m_json = models.JSONField()

    class Meta:
        managed = True
        db_table = 'Media'


class Chat(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=255)
    c_profile_photo = models.ForeignKey('Picture', models.DO_NOTHING, db_column='m_profile_photo', blank=True, null=True)
    c_description = models.CharField(max_length=255)
    c_create_time = models.DateTimeField()
    c_last_modify_date = models.DateTimeField()
    c_father_group_id = models.ForeignKey('Group', models.DO_NOTHING)

    c_medias = models.ManyToManyField(Media, related_name='m_chats')
    c_users = models.ManyToManyField('User', related_name='u_chats')

    class Meta:
        managed = True
        db_table = 'Chat'


class Group(models.Model):
    g_id = models.AutoField(primary_key=True)
    g_name = models.CharField(max_length=255)
    g_profile_photo = models.ForeignKey('Picture', models.DO_NOTHING, db_column='m_profile_photo', blank=True, null=True)
    g_description = models.CharField(max_length=255)
    g_create_time = models.DateTimeField()
    g_last_modify_time = models.DateTimeField()

    g_medias = models.ManyToManyField(Media, related_name='m_groups')
    g_users = models.ManyToManyField('User', related_name='u_groups')

    class Meta:
        managed = True
        db_table = 'Group'


class Picture(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_content = models.ImageField(upload_to=settings.STATIC_ROOT)
    p_father_text_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Picture'


class Report(models.Model):
    r_id = models.AutoField(primary_key=True)
    r_user = models.ForeignKey('User', models.DO_NOTHING)
    r_text = models.ForeignKey('Text', models.DO_NOTHING)
    r_details = models.TextField()

    class Meta:
        managed = True
        db_table = 'Report'


class Text(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_type = models.IntegerField()
    t_user = models.ForeignKey('User', models.DO_NOTHING)
    t_media = models.ForeignKey('Media', models.DO_NOTHING)
    t_rate = models.FloatField(blank=True, null=True)
    t_like = models.IntegerField(blank=True, null=True)
    t_dislike = models.IntegerField(blank=True, null=True)
    t_description = models.TextField(blank=True, null=True)
    t_topic = models.CharField(max_length=255, blank=True, null=True)
    t_father = models.ForeignKey('self', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'Text'


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=255)
    u_password = models.CharField(max_length=255)
    u_profile_photo = models.ForeignKey(Picture, models.DO_NOTHING, db_column='u_profile_photo', blank=True, null=True)
    u_email = models.EmailField(max_length=255, blank=True, null=True)

    u_medias = models.ManyToManyField(Media, related_name='m_users')

    class Meta:
        managed = True
        db_table = 'User'







########################################################################################################################
# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group'
#
#
# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)
#
#
# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)
#
#
# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user'
#
#
# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)
#
#
# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)
#
#
# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'
#
#
# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)
#
#
# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_migrations'
#
#
# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_session'