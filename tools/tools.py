from models.models import *

ERR_REQUEST_METHOD_WRONG = 'ERR_REQUEST_METHOD_WRONG'
ERR_USERNAME_EXISTS = 'ERR_USERNAME_EXISTS'
ERR_PASSWORD_NOT_SAME = 'ERR_PASSWORD_NOT_SAME'
ERR_USER_NOT_EXISTS = 'ERR_USER_NOT_EXISTS'
ERR_PASSWORD_WRONG = 'ERR_PASSWORD_WRONG'
ERR_NO_CURRENT_USER = 'ERR_NO_CURRENT_USER'
ERR_MEDIA_NOT_EXISTS = 'ERR_MEDIA_NOT_EXISTS'
ERR_GROUP_NOT_EXISTS = 'ERR_GROUP_NOT_EXISTS'
ERR_CHAT_NOT_EXISTS = 'ERR_CHAT_NOT_EXISTS'
ERR_NOT_LOGGED_IN = 'ERR_NOT_LOGGED_IN'
ERR_OTHER = 'ERR_OTHER'
ERR_ALREADY_JOINED = 'ERR_ALREADY_JOINED'
ERR_NOT_JOINED = 'ERR_NOT_JOINED'

CUR_USER_ID = 'cur_user_id'
DEFAULT_PROFILE_PHOTO_ID = 4  # make this right before running !!!


def is_logged_in(request):
    return True  # Wrong !!!


def get_cur_user(request):
    return User.objects.get(u_id=6)  # Wrong !!!


def get_cur_user_id(request):
    return 6  # Wrong !!!


def get_chat_by_id(i):
    return Chat.objects.get(c_id=i)


def get_group_by_id(i):
    return Group.objects.get(g_id=i)


def get_media_by_id(i):
    return Media.objects.get(m_id=i)


def get_text_by_id(i):
    return Text.objects.get(t_id=i)


def get_report_by_id(i):
    return Report.objects.get(r_id=i)


def basic_check(request):
    return request.method == 'POST' and is_logged_in(request)
