from django.db import models


class Media(models.Model):
    # public
    m_id = models.AutoField(primary_key=True)
    m_name = models.CharField(max_length=255, default='')
    m_type = models.IntegerField(default=0)  # 1 -> movie  2 -> series  3 -> book
    m_rate = models.FloatField(default=0)
    m_rate_num = models.IntegerField(default=0)
    m_heat = models.IntegerField(default=0)
    m_profile_photo = models.ForeignKey('Picture', models.DO_NOTHING, db_column='m_profile_photo', default=None, null=True)
    m_genre = models.CharField(max_length=255, default='')
    m_description = models.TextField(max_length=65535, default='')
    m_year = models.IntegerField(default=0)
    m_region = models.CharField(max_length=255, default='')
    # movie & series
    m_director = models.CharField(max_length=255, default='')
    m_actor = models.CharField(max_length=255, default='')
    m_episode_num = models.IntegerField(default=0)
    m_duration = models.IntegerField(default=0)
    # book
    m_author = models.CharField(max_length=255, default='')
    m_characters = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'Media'

    def to_dict(self):
        re = {
            'm_id': self.m_id,
            'm_name': self.m_name,
            'm_type': self.m_type,
            'm_rate': self.m_rate,
            'm_rate_num': self.m_rate_num,
            'm_heat': self.m_heat,
            'm_genre': self.m_genre,
            'm_description': self.m_description,
            'm_year': self.m_year,
            'm_region': self.m_region,
            'm_director': self.m_director,
            'm_actor': self.m_actor,
            'm_episode_num': self.m_episode_num,
            'm_duration': self.m_duration,
            'm_author': self.m_author,
            'm_characters': self.m_characters,
        }
        if self.m_profile_photo is not None:
            re['m_profile_photo'] = self.m_profile_photo.p_content.url
        else:
            re['m_profile_photo'] = ''
        return re


class Chat(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=255)
    c_profile_photo = models.ForeignKey('Picture', models.DO_NOTHING, db_column='m_profile_photo', default=None, null=True)
    c_description = models.CharField(max_length=255, default='')
    c_create_time = models.DateTimeField(auto_now=True)
    c_last_modify_time = models.DateTimeField(auto_now=True)
    c_father_group = models.ForeignKey('Group', models.DO_NOTHING, default=None)
    c_users_num = models.IntegerField(default=0)

    c_medias = models.ManyToManyField(Media, related_name='m_chats', through='MediaChat')  # 话题和作品的关系
    c_users = models.ManyToManyField('User', related_name='u_chats', through='UserChat')

    class Meta:
        managed = True
        db_table = 'Chat'

    def to_dict(self):
        re = {
            'c_id': self.c_id,
            'c_name': self.c_name,
            'c_description': self.c_description.__str__(),
            'c_create_time': self.c_create_time.__str__(),
            'c_last_modify_time': self.c_last_modify_time.__str__(),
            'c_users_num': self.c_users_num
        }
        if self.c_profile_photo is not None:
            re['c_profile_photo'] = self.c_profile_photo.p_content.url
        else:
            re['c_profile_photo'] = ''
        return re


class Group(models.Model):
    g_id = models.AutoField(primary_key=True)
    g_name = models.CharField(max_length=255)
    g_profile_photo = models.ForeignKey('Picture', models.DO_NOTHING, db_column='g_profile_photo', default=None, null=True)
    g_description = models.CharField(max_length=255, default='')
    g_create_time = models.DateTimeField(auto_now=True)
    g_last_modify_time = models.DateTimeField(auto_now=True)
    g_users_num = models.IntegerField(default=0)
    g_tag = models.CharField(max_length=255, default='')

    g_medias = models.ManyToManyField(Media, related_name='m_groups', through='MediaGroup')
    g_users = models.ManyToManyField('User', related_name='u_groups', through='UserGroup')

    class Meta:
        managed = True
        db_table = 'Group'

    def to_dict(self):
        re = {
            'g_id': self.g_id,
            'g_name': self.g_name,
            'g_description': self.g_description,
            'g_create_time': self.g_create_time.__str__(),
            'g_last_modify_time': self.g_last_modify_time.__str__(),
            'g_users_num': self.g_users_num,
            'g_tag': self.g_tag
        }
        if self.g_profile_photo is not None:
            re['g_profile_photo'] = self.g_profile_photo.p_content.url
        else:
            re['g_profile_photo'] = ''
        return re


class Picture(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_content = models.ImageField(upload_to='')
    p_father_text = models.ForeignKey('Text', models.DO_NOTHING, db_column='p_father_text', default=None, null=True)

    class Meta:
        managed = True
        db_table = 'Picture'

    def to_dict(self):
        return {
            'p_id': self.p_id,
            'p_content': self.p_content.url,
        }


class Report(models.Model):
    r_id = models.AutoField(primary_key=True)
    r_user = models.ForeignKey('User', models.DO_NOTHING, default=None)
    r_text = models.ForeignKey('Text', models.DO_NOTHING, default='')
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
    t_rate = models.FloatField(default=None)
    t_like = models.IntegerField(default=0)
    t_dislike = models.IntegerField(default=0)
    t_description = models.TextField(default='')
    t_topic = models.CharField(max_length=255, default='')
    t_create_time = models.DateTimeField(auto_now=True)
    # text -> media                     1
    t_media = models.ForeignKey('Media', models.DO_NOTHING, default=None, blank=True, null=True)
    # text -> post -> chat -> group     2
    t_text = models.ForeignKey('self', models.DO_NOTHING, default=None, blank=True, null=True)
    t_floor = models.IntegerField(default=0, blank=True, null=True)
    # text -> text                      3
    t_post = models.ForeignKey('Post', models.DO_NOTHING, default=None, blank=True, null=True)

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
            't_create_time': self.t_create_time.__str__()
        }


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=255)
    u_password = models.CharField(max_length=255)
    u_profile_photo = models.ForeignKey(Picture, models.DO_NOTHING, db_column='u_profile_photo', default=None, null=True)
    u_email = models.EmailField(max_length=255, default='')

    u_medias = models.ManyToManyField(Media, related_name='m_users', through='UserMedia')
    u_texts = models.ManyToManyField(Text, related_name='t_users', through='UserText')

    class Meta:
        managed = True
        db_table = 'User'

    def to_dict(self):
        re = {
            'u_id': self.u_id,
            'u_name': self.u_name,
            'u_password': self.u_password,
            'u_email': self.u_email.__str__()
        }
        if self.u_profile_photo is not None:
            re['u_profile_photo'] = self.u_profile_photo.p_content.url
        else:
            re['u_profile_photo'] = ''
        return re


class Post(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_title = models.CharField(max_length=255, default='')
    p_like = models.IntegerField(default=0)
    p_dislike = models.IntegerField(default=0)
    p_create_time = models.DateTimeField(auto_now=True)
    p_chat = models.ForeignKey('Chat', models.DO_NOTHING)
    p_first_floor_text = models.ForeignKey('Text', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'Post'

    def to_dict(self):
        return {
            'p_id': self.p_id,
            'p_title': self.p_title,
            'p_like': self.p_like,
            'p_dislike': self.p_dislike,
            'p_create_time': self.p_create_time.__str__()
        }


class UserText(models.Model):
    text = models.ForeignKey(Text, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    is_liked = models.IntegerField(default=0)
    is_disliked = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'UserText'


class UserMedia(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    media = models.ForeignKey(Media, models.DO_NOTHING)
    is_in_collection = models.IntegerField(default=0)
    is_to_be_watched = models.IntegerField(default=0)
    is_watching = models.IntegerField(default=0)
    is_watched = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'UserMedia'


class UserGroup(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    group = models.ForeignKey(Group, models.DO_NOTHING)
    is_admin = models.IntegerField(default=0)
    join_time = models.DateTimeField(auto_now=True)
    user_heat = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'UserGroup'


class UserChat(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    chat = models.ForeignKey(Chat, models.DO_NOTHING)
    is_admin = models.IntegerField(default=0)
    join_time = models.DateTimeField(auto_now=True)
    user_heat = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'UserChat'


class MediaGroup(models.Model):
    media = models.ForeignKey(Media, models.DO_NOTHING)
    group = models.ForeignKey(Group, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'MediaGroup'


class MediaChat(models.Model):
    media = models.ForeignKey(Media, models.DO_NOTHING)
    chat = models.ForeignKey(Chat, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'MediaChat'
