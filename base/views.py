import difflib
import random
from tools.mjorah7 import *
from tools.imports import *


def query_base(request):
    if request.method == 'POST':
        re_user = _query_user(request)
        re_chat = _query_chat(request)
        re_group = _query_group(request)
        re_media = _query_media(request)
        re = {
            'msg': 0,
            'data': {
                'user': re_user,
                'chat': re_chat,
                'group': re_group,
                'media': re_media
            }
        }
    else:
        re = {'msg': ERR_REQUEST_METHOD_WRONG}
    return HttpResponse(json.dumps(re))


def query_user(request):
    return HttpResponse(json.dumps(_query_user(request)))


def _query_user(request):
    re = {}
    if request.method == 'POST':
        qstr = request.POST['qstr']
        data = User.objects.filter(u_name__icontains=qstr)
        data = sorted(data, key=lambda x: weight(qstr, x.u_name))
        re['msg'] = 0
        result = []
        for item in data:
            result.append(item.to_dict())
        re['data'] = result
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return re


def query_post(request):
    return HttpResponse(json.dumps(_query_post(request)))


def _query_post(request):
    re = []
    if request.method == 'POST':
        qstr = request.POST['qstr']
        user = get_cur_user(request)
        ################################
        # print(qstr)
        ################################
        data = Post.objects.filter(Q(p_title__icontains=qstr))
        data = sorted(data, key=lambda x: weight(qstr, x.p_title))
        result = []
        for post in data:
            tmp = post.to_dict()
            tmp.update({
                'userIsAdmin': 0,
                'userIsLz': 0,
                'userLike': 0,
                'userDislike': 0,
                'userFav': 0
            })
            if UserPost.objects.filter(user=user, post=post, is_liked=1):
                tmp['userLike'] = 1
            if UserPost.objects.filter(user=user, post=post, is_disliked=1):
                tmp['userDislike'] = 1
            if UserPost.objects.filter(user=user, post=post, is_favorite=1):
                tmp['userFav'] = 1
            if post.p_user == user:
                tmp['userIsLz'] = 1
            if UserGroup(user=user, group=get_group_by_id(post.p_group.g_id), is_admin=1):
                tmp['userIsAdmin'] = 1
            result.append(tmp)
        re = result
        ################################
        # print(re)
        ################################
    return re


def query_chat(request):
    return HttpResponse(json.dumps(_query_chat(request)))


def _query_chat(request):
    re = []
    if request.method == 'POST':
        qstr = request.POST['qstr']
        user = get_cur_user(request)
        ################################
        # print(qstr)
        ################################
        data = Chat.objects.filter(Q(c_name__icontains=qstr) |
                                   Q(c_description__icontains=qstr))
        data = sorted(data, key=lambda x: weight(qstr, x.c_name + x.c_description))
        result = []
        for chat in data:
            tmp = chat.to_dict()
            tmp.update({
                'follow': get_chat_follow_num(chat),
                'post': get_chat_post_num(chat)
            })
            result.append(tmp)
        re = result
        ################################
        # print(re)
        ################################
    return re


def query_group(request):
    return HttpResponse(json.dumps(_query_group(request)))


def _query_group(request):
    re = []
    if request.method == 'POST':
        qstr = request.POST['qstr']
        ################################
        # print(qstr)
        ################################
        user = get_cur_user(request)
        data = Group.objects.filter(Q(g_name__icontains=qstr) |
                                    Q(g_description__icontains=qstr) |
                                    Q(g_tag__icontains=qstr))
        data = sorted(data, key=lambda x: weight(qstr, x.g_name + x.g_description))
        re_data = []
        for group in data:
            tmp = group.to_dict()
            tmp.update({
                'userIsAdmin': 0,
                'userInGroup': 0
            })
            if user_is_group_admin(user, group):
                tmp['userIsAdmin'] = 1
            if user_in_group(user, group):
                tmp['userInGroup'] = 1
            re_data.append(tmp)
        re = re_data
        ################################
        # print(re)
        ################################
    return re


def query_media(request):
    return HttpResponse(json.dumps(_query_media(request)))


def _query_media(request):
    re = {}
    if request.method == 'POST':
        qstr = request.POST['qstr']
        op = request.POST['op']
        print(op, int(int(op)+1))
        data = list(Media.objects.filter(Q(m_name__icontains=qstr) | Q(m_description__icontains=qstr)
                                         | Q(m_genre__icontains=qstr) | Q(m_region__icontains=qstr)
                                         | Q(m_director__icontains=qstr) | Q(m_actor__icontains=qstr)
                                         | Q(m_author__icontains=qstr)).filter(Q(m_type=op) | Q(m_type=int(int(op)+1))))
        data = sorted(data, key=lambda x: weight(qstr,
                                                 x.m_name + x.m_description + x.m_genre + x.m_region + x.m_director if x.m_director else '' + x.m_actor if x.m_actor else '' + x.m_author if x.m_author else ''))
        re['msg'] = 0
        result = []
        for item in data:
            result.append(item.to_dict())
        re['data'] = result
        print(len(result))
        print(result)
        # print([x['m_id'] for x in result])
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return re


def weight(str1, str2):
    seq_matcher = difflib.SequenceMatcher(None, str1, str2)
    return round(seq_matcher.ratio() * max(len(str1), len(str2)))


def base_movie_series_list(request):
    re = {}
    if basic_check(request):
        my_list = list(Media.objects.filter(Q(m_type=1) | Q(m_type=2)))[:6]
        my_list = sorted(my_list, key=lambda x: x.m_rate)
        my_list = [
            {
                'id': x.m_id,
                'cardImage': settings.ROOT_URL + get_one_preview_url(x),
                'miniImage': settings.ROOT_URL + x.m_profile_photo.p_content.url,
                'name': x.m_name,
                'text': x.m_description[:15]
            } for x in my_list
        ]
        re['msg'] = 0
        re['list'] = my_list
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def base_book_list(request):
    re = {}
    if basic_check(request):
        my_list = list(Media.objects.filter(m_type=3))[:12]
        my_list = sorted(my_list, key=lambda x: x.m_rate)
        my_list = [
            {
                'id': x.m_id,
                'image': settings.ROOT_URL + x.m_profile_photo.p_content.url,
                'rate': get_media_ratio(x),
                'name': x.m_name,
                'text': x.m_description[:15],
                'star': x.m_author
            } for x in my_list
        ]
        re['msg'] = 0
        re['list'] = my_list
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_one_preview_url(media):
    return list(Picture.objects.filter(p_media=media))[0].p_content.url


def get_media_ratio(media):
    _list = list(UserMedia.objects.filter(media=media))
    ###################################################
    # print(media.m_id, _list)
    ###################################################
    if len(_list) == 0:
        return '0.0%'
    cnt = 0
    for item in _list:
        if item.rate >= 8:
            cnt += 1
    return str(round(100.0 * cnt / len(_list), 1)) + '%'


def col_media_series(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        _list = list(Media.objects.filter(m_type__lt=2))
        _list = [x.to_dict() for x in _list]
        for item in _list:
            item.update({
                'is_fav': 0
            })
            if UserMedia.objects.filter(user=user, media=get_media_by_id(item['m_id']), is_in_collection=1):
                item['is_fav'] = 1
        random.shuffle(_list)
        re['msg'] = 0
        re['list'] = _list[:6]
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def col_book(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        _list = list(Media.objects.filter(m_type=3))
        _list = [x.to_dict() for x in _list]
        for item in _list:
            item.update({
                'is_fav': 0
            })
            if UserMedia.objects.filter(user=user, media=get_media_by_id(item['m_id']), is_in_collection=1):
                item['is_fav'] = 1
        random.shuffle(_list)
        re['msg'] = 0
        re['list'] = _list[:6]
        ###################################
        # print(_list)
        ###################################
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def col_chat(request):
    re = {}
    if basic_check(request):
        _list = list(Chat.objects.filter())
        random.shuffle(_list)
        _list = [x.to_dict() for x in _list][:5]
        re['msg'] = 0
        re['chats'] = _list
        print(re)
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def col_group(request):
    re = {}
    if basic_check(request):
        _list = list(Group.objects.filter())
        random.shuffle(_list)
        _list = [x.to_dict() for x in _list][:6]
        re['msg'] = 0
        re['groups'] = _list
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_um_rate(request):
    user = get_cur_user(request)
    media = get_media_by_id(request.POST['m_id'])
    if UserMedia.objects.filter(user=user, media=media):
        um = UserMedia.objects.get(user=user, media=media)
        return HttpResponse(json.dumps(um.rate))
    else:
        return HttpResponse(json.dumps(0))
