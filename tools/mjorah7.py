from tools.imports import *


def user_is_group_admin(user, group):
    if UserGroup(user=user, group=group, is_admin=1):
        return True
    return False


def user_in_group(user, group):
    if UserGroup(user=user, group=group):
        return True
    return False


def get_chat_follow_num(chat):
    return len(UserChat.objects.filter(chat=chat))


def get_chat_post_num(chat):
    return len(Post.objects.filter(p_chat=chat))
