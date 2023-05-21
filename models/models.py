# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.conf import settings
from django.db import models


class Media(models.Model):
    # public
    m_id = models.AutoField(primary_key=True)
    m_name = models.CharField(max_length=255)
    m_type = models.IntegerField()  # 1 -> movie  2 -> series  3 -> book
    m_rate = models.FloatField(default=None)
    m_rate_num = models.IntegerField(default=0)
    m_heat = models.IntegerField(default=0)
    m_profile_photo = models.ForeignKey('Picture', models.DO_NOTHING, db_column='m_profile_photo', default=None)
    m_genre = models.CharField(max_length=255, default=None)
    m_description = models.TextField(max_length=65535, default=None)
    m_time = models.IntegerField(default=None)
    m_region = models.CharField(max_length=255, default=None)
    # movie
    m_director = models.CharField(max_length=255, default=None)
    m_actor = models.CharField(max_length=255, default=None)
    # series
    m_episode_num = models.IntegerField(default=None)
    # book
    m_author = models.CharField(max_length=255, default=None)

    class Meta:
        managed = True
        db_table = 'Media'

    def to_dict(self):
        return {
            'm_id': self.m_id,
            'm_name': self.m_name,
            'm_type': self.m_type,
            'm_rate': self.m_rate,
            'm_rate_num': self.m_rate_num,
            'm_heat': self.m_heat,
            'm_profile_photo': self.m_profile_photo.p_content.url,
            'm_genre': self.m_genre,
            'm_description': self.m_description,
            'm_time': self.m_time,
            'm_region': self.m_region,
            'm_director': self.m_director,
            'm_actor': self.m_actor,
            'm_episode_num': self.m_episode_num,
            'm_author': self.m_author
        }


class Chat(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=255)
    c_profile_photo = models.ForeignKey('Picture', models.DO_NOTHING, db_column='m_profile_photo', default=None)
    c_description = models.CharField(max_length=255)
    c_create_time = models.DateTimeField(auto_now=True)
    c_last_modify_date = models.DateTimeField(auto_now=True)
    c_father_group = models.ForeignKey('Group', models.DO_NOTHING, default=None)

    c_medias = models.ManyToManyField(Media, related_name='m_chats')
    c_users = models.ManyToManyField('User', related_name='u_chats')

    class Meta:
        managed = True
        db_table = 'Chat'

    def to_dict(self):
        return {
            'c_id': self.c_id,
            'c_name': self.c_name,
            'c_profile_photo': self.c_profile_photo.p_content.url,
            'c_description': self.c_description,
            'c_create_time': self.c_create_time,
            'c_father_group': self.c_father_group.g_id
        }


class Group(models.Model):
    g_id = models.AutoField(primary_key=True)
    g_name = models.CharField(max_length=255)
    g_profile_photo = models.ForeignKey('Picture', models.DO_NOTHING, db_column='g_profile_photo', default=None)
    g_description = models.CharField(max_length=255)
    g_create_time = models.DateTimeField(auto_now=True)
    g_last_modify_time = models.DateTimeField(auto_now=True)

    g_medias = models.ManyToManyField(Media, related_name='m_groups')
    g_users = models.ManyToManyField('User', related_name='u_groups')

    class Meta:
        managed = True
        db_table = 'Group'

    def to_dict(self):
        return {
            'g_id': self.g_id,
            'g_name': self.g_name,
            'g_profile_photo': self.g_profile_photo.p_content.url,
            'g_description': self.g_description,
            'g_create_time': self.g_create_time,
            'g_last_modify_time': self.g_last_modify_time
        }


class Picture(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_content = models.ImageField(upload_to='')
    p_father_text = models.ForeignKey('Text', models.DO_NOTHING, db_column='p_father_text', default=None)

    class Meta:
        managed = True
        db_table = 'Picture'

    def to_dict(self):
        return {
            'p_id': self.p_id,
            'p_content': self.p_content.url,
            'p_father_text': self.p_father_text.t_id
        }


class Report(models.Model):
    r_id = models.AutoField(primary_key=True)
    r_user = models.ForeignKey('User', models.DO_NOTHING, default=None)
    r_text = models.ForeignKey('Text', models.DO_NOTHING, default=None)
    r_details = models.TextField()

    class Meta:
        managed = True
        db_table = 'Report'

    def to_dict(self):
        return {
            'r_id': self.r_id,
            'r_user': self.r_user.u_id,
            'r_text': self.r_text.t_id,
            'r_details': self.r_details
        }


class Text(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_type = models.IntegerField()  # 1 -> 长评  2 -> 帖子  3 -> 回复
    t_user = models.ForeignKey('User', models.DO_NOTHING, default=None)
    t_media = models.ForeignKey('Media', models.DO_NOTHING, default=None)
    t_rate = models.FloatField(default=None)
    t_like = models.IntegerField(default=0)
    t_dislike = models.IntegerField(default=0)
    t_description = models.TextField(default='')
    t_topic = models.CharField(max_length=255, default=None)
    t_father = models.ForeignKey('self', models.DO_NOTHING, default=None)

    class Meta:
        managed = True
        db_table = 'Text'

    def to_dict(self):
        return {
            't_id': self.t_id,
            't_type': self.t_type,
            't_user': self.t_user.u_id,
            't_media': self.t_media.m_id,
            't_rate': self.t_rate,
            't_like': self.t_like,
            't_dislike': self.t_dislike,
            't_description': self.t_description,
            't_topic': self.t_topic,
            't_father': self.t_father.t_id
        }


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=255)
    u_password = models.CharField(max_length=255)
    u_profile_photo = models.ForeignKey(Picture, models.DO_NOTHING, db_column='u_profile_photo', default=None)
    u_email = models.EmailField(max_length=255, default=None)

    u_medias = models.ManyToManyField(Media, related_name='m_users', through='UserMedia')
    u_texts = models.ManyToManyField(Text, related_name='t_users')

    class Meta:
        managed = True
        db_table = 'User'

    def to_dict(self):
        return {
            'u_id': self.u_id,
            'u_name': self.u_name,
            'u_password': self.u_password,
            'u_profile_photo': self.u_profile_photo.p_content.url,
            'u_email': self.u_email.__str__()
        }


class UserMedia(models.Model):
    type = models.IntegerField()

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
