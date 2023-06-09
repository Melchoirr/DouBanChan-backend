from django.contrib.auth.models import User
from django.db import models

from DouBanChan_Backend import settings


class Media(models.Model):
    # public
    m_id = models.AutoField(primary_key=True)
    m_name = models.CharField(max_length=255, default='')
    m_type = models.IntegerField(default=0)  # 1 -> movie  2 -> series  3 -> book
    m_rate = models.FloatField(default=0)
    m_rate_num = models.IntegerField(default=0)
    m_profile_photo = models.ForeignKey('Picture', models.DO_NOTHING, db_column='m_profile_photo', default=None,
                                        null=True)
    m_genre = models.CharField(max_length=255, default='')
    m_description = models.TextField(max_length=65535, default='')
    m_year = models.IntegerField(default=0)
    m_region = models.CharField(max_length=255, default='')
    m_language = models.CharField(max_length=255, default='')
    m_heat = models.IntegerField(default=0)
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
            re['m_profile_photo'] = settings.ROOT_URL + self.m_profile_photo.p_content.url
        else:
            re['m_profile_photo'] = settings.ROOT_URL
        return re


class Chat(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=255, default='')
    c_profile_photo = models.ForeignKey('Picture', models.DO_NOTHING, db_column='m_profile_photo', default=None,
                                        null=True)
    c_description = models.CharField(max_length=255, default='')
    c_create_time = models.DateTimeField(auto_now_add=True)
    c_last_modify_time = models.DateTimeField(auto_now_add=True)
    c_father_group = models.ForeignKey('Group', models.CASCADE, default=None)
    c_heat = models.IntegerField(default=0)
    c_tag = models.CharField(max_length=255, default='')

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
            'c_heat': self.c_heat,
        }
        if self.c_profile_photo is not None:
            re['c_profile_photo'] = self.c_profile_photo.p_content.url
        else:
            re['c_profile_photo'] = ''
        if self.c_father_group is not None:
            re['c_father_group'] = self.c_father_group.to_dict(),
        return re


class Group(models.Model):
    g_id = models.AutoField(primary_key=True)
    g_name = models.CharField(max_length=255)
    g_profile_photo = models.ForeignKey('Picture', models.DO_NOTHING, db_column='g_profile_photo', default=None,
                                        null=True)
    g_description = models.CharField(max_length=255, default='')
    g_create_time = models.DateTimeField(auto_now_add=True)
    g_last_modify_time = models.DateTimeField(auto_now_add=True)
    g_users_num = models.IntegerField(default=0)
    g_tag = models.CharField(max_length=255, default='')
    g_nickname = models.CharField(max_length=255, default='人')

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
            'p_content': settings.ROOT_URL + self.p_content.url,
        }


class Text(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_type = models.IntegerField()  # 1 -> 长评  2 -> 帖子  3 -> 回复
    t_user = models.ForeignKey('User', models.DO_NOTHING, default=None)
    t_rate = models.FloatField(default=0)
    t_like = models.IntegerField(default=0)
    t_dislike = models.IntegerField(default=0)
    t_description = models.TextField(default='')
    t_topic = models.CharField(max_length=255, default='')
    t_create_time = models.DateTimeField(auto_now_add=True)
    # text -> media                     1
    t_media = models.ForeignKey('Media', models.CASCADE, default=None, blank=True, null=True)
    # text -> post -> chat -> group     2
    t_post = models.ForeignKey('Post', on_delete=models.CASCADE, default=None, blank=True, null=True)
    t_floor = models.IntegerField(default=0, blank=True, null=True)
    # text -> text                      3
    t_text = models.ForeignKey('self', models.CASCADE, default=None, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Text'

    def to_dict(self):
        re = {
            't_id': self.t_id,
            't_type': self.t_type,
            't_topic': self.t_topic,
            't_user': self.t_user.to_dict(),  # 不仅要返回id（可以构成新的url请求），还要返回全部信息以便展示
            't_rate': self.t_rate,
            't_like': self.t_like,
            't_dislike': self.t_dislike,
            't_description': self.t_description,
            't_create_time': self.t_create_time.__str__(),
        }
        if self.t_media is not None:
            re['t_media'] = self.t_media.to_dict()  #
        if self.t_floor != 0:
            re['t_floor'] = self.t_floor
            re['t_post'] = self.t_post.to_dict()

        return re

    def like(self):
        self.t_like += 1
        self.save()

    def dislike(self):
        self.t_dislike += 1
        self.save()


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=255)
    u_password = models.CharField(max_length=255)
    u_profile_photo = models.ForeignKey(Picture, models.DO_NOTHING, db_column='u_profile_photo', default=None,
                                        null=True)
    u_email = models.EmailField(max_length=255, default='')
    u_authority = models.IntegerField(default=1)  # 1 : normal 2 : admin
    u_medias = models.ManyToManyField(Media, related_name='m_users', through='UserMedia')
    u_texts = models.ManyToManyField(Text, related_name='t_users', through='UserText')
    u_posts = models.ManyToManyField('Post', related_name='p_users', through='UserPost')

    class Meta:
        managed = True
        db_table = 'User'

    def to_dict(self):
        re = {
            'u_id': self.u_id,
            'u_name': self.u_name,
            # 'u_password': self.u_password, 没必要吧？
            'u_email': self.u_email.__str__()
        }
        if self.u_profile_photo is not None:
            re['u_profile_photo'] = settings.ROOT_URL + self.u_profile_photo.p_content.url
        else:
            re['u_profile_photo'] = ''
        return re


class Post(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_user = models.ForeignKey('User', models.CASCADE, default=None)
    p_title = models.CharField(max_length=255, default='')
    p_like = models.IntegerField(default=0)
    p_dislike = models.IntegerField(default=0)
    p_create_time = models.DateTimeField(auto_now_add=True)
    p_chat = models.ForeignKey('Chat', models.CASCADE, default=None, null=True)
    p_group = models.ForeignKey('Group', models.CASCADE, default=None, null=True)
    p_is_essence = models.IntegerField(default=0)  # key
    p_is_top = models.IntegerField(default=0)  # key
    p_floor_num = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'Post'

    def to_dict(self):
        re = {
            'p_id': self.p_id,
            'p_user': self.p_user.to_dict(),
            'p_title': self.p_title,
            'p_like': self.p_like,
            'p_dislike': self.p_dislike,
            'p_chat': self.p_chat.to_dict(),
            'p_first_floor_text': Text.objects.get(t_post=self, t_floor=1).to_dict(),
            'p_create_time': self.p_create_time.__str__(),
            'p_floor_num': self.p_floor_num,
            'p_is_essence': self.p_is_essence,
            'p_is_top': self.p_is_top,
        }
        if self.p_group is not None:
            re['p_group'] = self.p_group.to_dict()
        return re


class Message(models.Model):
    m_id = models.AutoField(primary_key=True, default=None)
    m_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user', default=None, blank=True, null=True)
    m_applier = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='applier', default=None, blank=True, null=True)
    m_text = models.ForeignKey(Text, on_delete=models.DO_NOTHING, default=None, blank=True, null=True)
    m_post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, default=None, blank=True, null=True)
    m_title = models.CharField(max_length=255)
    m_content = models.CharField(max_length=255)
    m_type = models.IntegerField()  # 1：申请成为管理员 2：举报帖子 3：举报文本 4：消息（申请管理员成功或者失败，举报成功或者失败）发过来的时候怎么处理（if not null）
    # 返回时分类依据：消息内部分类
    # 怎么做到给文章点赞返回信息？ 在点赞的时候
    # 评论
    # 删除message？

    class Meta:
        managed = True
        db_table = 'Apply'

    def to_dict(self):
        re = {
            'm_id': self.m_id,
            'm_user': self.m_user.to_dict(),
            'm_title': self.m_title,
            'm_type': self.m_type,
            'm_content': self.m_content,
        }
        if self.m_applier is not None:
            re['m_applier'] = self.m_applier.to_dict()
        if self.m_text is not None:
            re['m_text'] = self.m_text.to_dict()
        if self.m_post is not None:
            re['m_post'] = self.m_post.to_dict()
        return re


class UserText(models.Model):
    text = models.ForeignKey(Text, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    is_liked = models.IntegerField(default=0)
    is_disliked = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'UserText'


class UserPost(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    post = models.ForeignKey(Post, models.DO_NOTHING)
    is_liked = models.IntegerField(default=0)
    is_disliked = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'UserPost'


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
    is_applying = models.IntegerField(default=0)
    is_member = models.IntegerField(default=0)
    join_time = models.DateTimeField(auto_now_add=True)
    user_heat = models.IntegerField(default=0)  # ?

    class Meta:
        managed = True
        db_table = 'UserGroup'


class UserChat(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    chat = models.ForeignKey(Chat, models.DO_NOTHING)
    is_admin = models.IntegerField(default=0)
    join_time = models.DateTimeField(auto_now_add=True)
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
