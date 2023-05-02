# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Group(models.Model):
    g_id = models.AutoField(primary_key=True)
    g_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'Group'


class Media(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_name = models.CharField(max_length=255)
    m_type = models.IntegerField()
    m_rate = models.FloatField(blank=True, null=True)
    m_rate_num = models.IntegerField(blank=True, null=True)
    m_heat = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Media'


class Mediatext(models.Model):
    mt_m = models.OneToOneField(Media, models.DO_NOTHING, primary_key=True)
    mt_t = models.ForeignKey('Text', models.DO_NOTHING)
    mt_time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'MediaText'
        unique_together = (('mt_m', 'mt_t'),)


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
    t_media_id = models.IntegerField()
    t_rate = models.FloatField()
    t_like = models.IntegerField(blank=True, null=True)
    t_dislike = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Text'


class Textreport(models.Model):
    tr_t = models.OneToOneField(Text, models.DO_NOTHING, primary_key=True)
    tr_r = models.ForeignKey(Report, models.DO_NOTHING)
    tr_time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'TextReport'


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=255)
    u_password = models.CharField(max_length=255)
    u_prifole_photo = models.TextField(blank=True, null=True)
    u_email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'User'


class Usergroup(models.Model):
    ug_u = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    ug_g = models.ForeignKey(Group, models.DO_NOTHING)
    ug_is_admin = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'UserGroup'
        unique_together = (('ug_u', 'ug_g'),)


class Usermedia(models.Model):
    um_u = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    um_m = models.ForeignKey(Media, models.DO_NOTHING)
    um_time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'UserMedia'


class Userreport(models.Model):
    ur_u = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    ur_r = models.ForeignKey(Report, models.DO_NOTHING)
    ur_time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'UserReport'


class Usertext(models.Model):
    ut_u = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    ut_t = models.ForeignKey(Text, models.DO_NOTHING)
    ut_time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'UserText'
