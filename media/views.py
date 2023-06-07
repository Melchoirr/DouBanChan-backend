import copy
from tools.imports import *
from tools.tools import *
from text.views import get_text_replies, get_text_status
from base.views import weight


def create_media(request):
    """
    /media/create POST
    create new media
    :param request: m_name m_type
    :return: json, msg = 0 on success
    """
    re = {}
    if request.method == 'POST':
        m_name = request.POST['m_name']
        m_type = request.POST['m_type']
        m_genre = request.POST['m_genre']
        m_description = request.POST['m_description']
        m_year = request.POST['m_year']
        m_director = request.POST['m_director']
        m_actor = request.POST['m_actor']
        m_region = request.POST['m_region']
        m_episode_num = request.POST['m_episode_num']
        m_duration = request.POST['m_duration']
        m_author = request.POST['m_author']
        m_characters = request.POST['m_characters']
        m_profile_photo = request.FILES['m_profile_photo']
        media = Media(m_name=m_name, m_type=m_type, m_profile_photo=m_profile_photo, m_genre=m_genre,
                      m_description=m_description, m_year=m_year, m_director=m_director, m_actor=m_actor, m_region=m_region,
                      m_episode_num=m_episode_num, m_duration=m_duration, m_author=m_author, m_characters=m_characters)
        media.save()
        re['media'] = media.to_dict()
        re['msg'] = 0
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def delete_media(request):
    """
    /media/delete POST
    delete media
    :param request: m_id
    :return: json, msg = 0 on success
    """
    re = {}
    if request.method == 'POST':
        media_id = request.POST['m_id']
        if not Media.objects.filter(m_id=media_id):
            re['msg'] = ERR_MEDIA_NOT_EXISTS
        else:
            media = Media.objects.get(m_id=media_id)
            media.delete()
            re['msg'] = 0
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def query_single_media(request):
    """
    /media/query_single POST
    query single media
    :param request: m_id
    :return: json, msg = 0 on success
    """
    re = {}
    if request.method == 'POST':
        m_id = request.POST.get('m_id')
        user = get_cur_user(request)
        if not Media.objects.filter(m_id=m_id):
            re['msg'] = ERR_MEDIA_NOT_EXISTS
        else:
            media = Media.objects.get(m_id=m_id)
            media.m_heat += 1
            media.save()
            re['msg'] = 0
            re['media'] = media.to_dict()
            tmp = []
            text_to_media = list(Text.objects.filter(t_media=media))
            if request.POST['u_id']:
                for item in text_to_media:
                    tt = {
                        'text': item.to_dict(),
                        'is_liked': 0,
                        'is_disliked': 0,
                        'replies': get_text_replies(item)
                    }
                    tt.update(get_text_status(user, item))
                    cur_user = User.objects.get(u_id=request.POST['u_id'])
                    if UserText.objects.filter(user=cur_user, text=item, is_liked=1):
                        tt['is_liked'] = 1
                    if UserText.objects.filter(user=cur_user, text=item, is_disliked=1):
                        tt['is_disliked'] = 1
                    tmp.append(tt)
            else:
                for item in text_to_media:
                    tmp.append({
                        'text': item.to_dict(),
                        'is_liked': 0,
                        'is_disliked': 0,
                        'replies': get_text_replies(item)
                    })
            re['text_by_time'] = copy.deepcopy(tmp)
            re['text_by_like'] = copy.deepcopy(tmp)
            re['text_by_time'] = sorted(re['text_by_time'], key=lambda x: x['text']['t_create_time'], reverse=True)
            re['text_by_like'] = sorted(re['text_by_like'], key=lambda x: x['text']['t_like'], reverse=True)
            re['m_chats'] = [x.to_dict() for x in list(media.m_chats.all())]
            re['m_preview'] = get_media_preview(m_id)
            re['rate'] = get_user_rate(user, media)
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def get_media_status(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        media = get_media_by_id(request.POST['m_id'])
        re['msg'] = 0
        if UserMedia.objects.filter(user=user, media=media):
            um = UserMedia.objects.get(user=user, media=media)
            re['is_in_collection'] = um.is_in_collection
            re['rate'] = um.rate
        else:
            re['is_in_collection'] = 0
            re['rate'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_user_rate(user, media):
    if UserMedia.objects.filter(user=user, media=media):
        um = UserMedia.objects.get(user=user, media=media)
        return um.rate
    return 0


def get_media_preview(m_id):
    media = get_media_by_id(m_id)
    previews = list(Picture.objects.filter(p_media=media))
    return [x.to_dict()['p_content'] for x in previews]


def media_filter(request):
    re = {}
    if basic_check(request):
        m_type = request.POST['m_type']
        m_genre = request.POST['m_genre']
        m_region = request.POST['m_region']
        m_year = request.POST['m_year']
        m_order = request.POST['m_order']
        ##############################################
        # print(m_type, m_genre, m_region, m_year, m_order)
        ##############################################
        if m_type == '电影':
            m_type = 1
        if m_type == '电视剧':
            m_type = 2
        if m_type == '图书':
            m_type = 3
        if m_genre == '全部':
            m_genre = ''
        if m_region == '全部':
            m_region = ''
        if m_year == '全部':
            start = 0
            end = 3000
        else:
            m_year = m_year[:-2]
            start = int(m_year) - 1
            end = int(m_year) + 10
        media = list(Media.objects.filter(
            m_type__icontains=m_type
        ).filter(
            m_genre__icontains=m_genre
        ).filter(
            m_region__icontains=m_region
        ).filter(
            m_year__gt=start
        ).filter(
            m_year__lt=end
        ))
        ##############################################
        # print(media)
        ##############################################
        media = [x.to_dict() for x in media]
        if m_order == 'timedown':  # 时间递减
            sorted(media, key=lambda x: x['m_year'].__str__())
            media.reverse()
        if m_order == 'timeup':  # 时间递增
            sorted(media, key=lambda x: x['m_year'].__str__())
        if m_order == 'ratedown':  # 评分递减
            sorted(media, key=lambda x: x['m_rate'])
            media.reverse()
        if m_order == 'rateup':  # 评分递增
            sorted(media, key=lambda x: x['m_rate'])
        re['msg'] = 0
        re['media'] = media
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def add_preview(request):
    re = {}
    if basic_check(request):
        m_id = request.POST['m_id']
        p_id = request.POST['p_id']
        media = get_media_by_id(m_id)
        picture = get_picture_by_id(p_id)
        picture.p_media = media
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_heat_comment(request):
    re = {}
    if basic_check(request):
        comments = list(Text.objects.filter(t_type=1))
        _comments = []
        for text in comments:
            if text.t_media.m_type == 1 or text.t_media.m_type == 2:
                _comments.append(text)
        _comments = [x.to_dict() for x in _comments]
        re['msg'] = 0
        re['heat_comment'] = _comments[:10]
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_heat_comment_for_book(request):
    re = {}
    if basic_check(request):
        comments = list(Text.objects.filter(t_type=1))
        _comments = []
        for text in comments:
            if text.t_media.m_type == 3:
                _comments.append(text)
        _comments = [x.to_dict() for x in _comments]
        re['msg'] = 0
        re['heat_comment'] = _comments[:10]
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def heated_movie(request):
    re = _heated_movie(request)
    return HttpResponse(json.dumps(re))


def _heated_movie(request):
    re = {}
    if basic_check(request):
        __heated_movie = list(Media.objects.filter(m_type=1))[:10]
        __heated_movie = [x.to_dict() for x in __heated_movie]
        user = get_cur_user(request)
        for xx in __heated_movie:
            if UserMedia.objects.filter(user=user, media=get_media_by_id(xx['m_id']), is_in_collection=1):
                xx.update({
                    'is_fav': 1
                })
            else:
                xx.update({
                    'is_fav': 0
                })
        __heated_movie = sorted(__heated_movie, key=lambda x: x['m_heat'], reverse=True)
        ##############################################
        # print(__heated_movie)
        ##############################################
        re['msg'] = 0
        re['heat_movie'] = __heated_movie
    else:
        re['msg'] = ERR_OTHER
    return re


def heated_series(request):
    re = _heated_series(request)
    return HttpResponse(json.dumps(re))


def _heated_series(request):
    re = {}
    if basic_check(request):
        __heated_series = list(Media.objects.filter(m_type=2))[:10]
        __heated_series = [x.to_dict() for x in __heated_series]
        user = get_cur_user(request)
        for x in __heated_series:
            if UserMedia.objects.filter(user=user, media=get_media_by_id(x['m_id']), is_in_collection=1):
                x.update({
                    'is_fav': 1
                })
            else:
                x.update({
                    'is_fav': 0
                })
        __heated_series = sorted(__heated_series, key=lambda x: x['m_heat'], reverse=True)
        re['msg'] = 0
        re['heat_series'] = __heated_series
    else:
        re['msg'] = ERR_OTHER
    return re


def heated_book(request):
    re = _heated_book(request)
    return HttpResponse(json.dumps(re))


def _heated_book(request):
    re = {}
    if basic_check(request):
        __heated_series = list(Media.objects.filter(m_type=3))[:10]
        __heated_series = [x.to_dict() for x in __heated_series]
        user = get_cur_user(request)
        for x in __heated_series:
            if UserMedia.objects.filter(user=user, media=get_media_by_id(x['m_id']), is_in_collection=1):
                x.update({
                    'is_fav': 1
                })
            else:
                x.update({
                    'is_fav': 0
                })
        __heated_series = sorted(__heated_series, key=lambda x: x['m_heat'], reverse=True)
        re['msg'] = 0
        re['heat_book'] = __heated_series
    else:
        re['msg'] = ERR_OTHER
    return re


def related_group(request):
    re = {}
    if basic_check(request):
        media = get_media_by_id(request.POST['m_id'])
        groups = list(Group.objects.filter(
            Q(g_name__icontains=media.m_name) or
            Q(g_description__icontains=media.m_name) or
            Q(g_tag__icontains=media.m_name)
        ))[:4]
        groups = sorted(groups, key=lambda x: weight(x.g_name + x.g_description + x.g_tag, media.m_name))
        re['groups'] = groups
        re['msg'] = 0
        print(re)
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def related_chat(request):
    re = {}
    if basic_check(request):
        media = get_media_by_id(request.POST['m_id'])
        chats = list(Chat.objects.filter(
            Q(c_name__icontains=media.m_name) or
            Q(c_description__icontains=media.m_name) or
            Q(c_tag__icontains=media.m_name)
        ))[:4]
        groups = sorted(chats, key=lambda x: weight(x.c_name + x.c_description + x.c_tag, media.m_name))
        re['chats'] = groups
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_status(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        text = get_text_by_id(request.POST['t_id'])
        re['msg'] = 0
        re.update(get_text_status(user, text))
    else:
        re['msg'] = 0
    return HttpResponse(json.dumps(re))


def set_watched(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        m_id = request.POST['m_id']
        op = int(request.POST['op'])
        media = Media.objects.get(m_id=m_id)
        if UserMedia.objects.filter(user=user, media=media):
            user_media = UserMedia.objects.get(user=user, media=media)
            user_media.is_watched = op
            user_media.save()
        else:
            user_media = UserMedia(user=user, media=media, is_watched=op)
            user_media.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def set_watching(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        m_id = request.POST['m_id']
        op = int(request.POST['op'])
        media = Media.objects.get(m_id=m_id)
        if UserMedia.objects.filter(user=user, media=media):
            user_media = UserMedia.objects.get(user=user, media=media)
            user_media.is_watching = op
            user_media.save()
        else:
            user_media = UserMedia(user=user, media=media, is_watching=op)
            user_media.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def set_to_be_watched(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        m_id = request.POST['m_id']
        op = int(request.POST['op'])
        media = Media.objects.get(m_id=m_id)
        if UserMedia.objects.filter(user=user, media=media):
            user_media = UserMedia.objects.get(user=user, media=media)
            user_media.is_to_be_watched = op
            user_media.save()
        else:
            user_media = UserMedia(user=user, media=media, is_to_be_watched=op)
            user_media.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def set_favourite(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        m_id = request.POST['m_id']
        op = int(request.POST['op'])
        media = Media.objects.get(m_id=m_id)
        if UserMedia.objects.filter(user=user, media=media):
            user_media = UserMedia.objects.get(user=user, media=media)
            user_media.is_in_collection = op
            user_media.save()
        else:
            user_media = UserMedia(user=user, media=media, is_in_collection=op)
            user_media.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def comment_media(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        m_id = request.POST['m_id']
        media = Media.objects.get(m_id=m_id)
        text = Text(t_type=1,
                    t_user=user,
                    t_media=media,
                    t_rate=request.POST['t_rate'],
                    t_like=0,
                    t_dislike=0,
                    t_description=request.POST['t_description'],
                    t_topic=request.POST['t_topic'], )
        text.save()
        media.m_rate = (media.m_rate * media.m_rate_num + float(request.POST['t_rate'])) / (media.m_rate_num + 1)
        media.m_rate_num += 1
        media.save()
        re['t_id'] = text.t_id
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def delete_comment(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        text = request.POST['t_id']
        if text.t_user == user:
            text.delete()
        else:
            re['msg'] = ERR_NOT_POSSESSION
            return HttpResponse(json.dumps(re))
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def rate_media(request):
    re = {}
    if basic_check(request):
        m_id = request.POST['m_id']
        user = get_cur_user(request)
        media = Media.objects.get(m_id=m_id)
        if UserMedia.objects.filter(user=user, media=media, rate__gt=0):
            uumm = UserMedia.objects.get(user=user, media=media, rate__gt=0)
            old_rate = uumm.rate
            media.m_rate = (media.m_rate * media.m_rate_num - float(old_rate) + float(request.POST['rate'])) / (media.m_rate_num)
        else:
            media.m_rate = (media.m_rate * media.m_rate_num + float(request.POST['rate'])) / (media.m_rate_num + 1)
            media.m_rate_num += 1
        media.save()
        if UserMedia.objects.filter(user=user, media=media):
            um = UserMedia.objects.get(user=user, media=media)
            um.rate = request.POST['rate']
            um.save()
        else:
            um = UserMedia(user=user, media=media, rate=request.POST['rate'])
            um.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def like_comment(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        t_id = request.POST['t_id']
        text = Text.objects.get(t_id=t_id)
        text.t_like += 1
        text.save()
        user_text = UserText(user=user, text=text, is_liked=1)
        user_text.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def dislike_comment(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        t_id = request.POST['t_id']
        text = Text.objects.get(t_id=t_id)
        text.t_dislike += 1
        text.save()
        user_text = UserText(user=user, text=text, is_disliked=1)
        user_text.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_ratio(request):
    media = get_media_by_id(request.POST['m_id'])
    _list = UserMedia.objects.filter(media=media)
    cnt, cnt12, cnt34, cnt56, cnt78, cnt90 = 0, 0, 0, 0, 0, 0
    for um in _list:
        cnt += 1
        if um.rate == 1 or um.rate == 2:
            cnt12 += 1
        if um.rate == 3 or um.rate == 4:
            cnt34 += 1
        if um.rate == 5 or um.rate == 6:
            cnt56 += 1
        if um.rate == 7 or um.rate == 8:
            cnt78 += 1
        if um.rate == 9 or um.rate == 10:
            cnt90 += 1
    return HttpResponse(json.dumps({
        '12': str(round(100.0 * cnt12 / cnt, 1)) + '%',
        '34': str(round(100.0 * cnt34 / cnt, 1)) + '%',
        '56': str(round(100.0 * cnt56 / cnt, 1)) + '%',
        '78': str(round(100.0 * cnt78 / cnt, 1)) + '%',
        '90': str(round(100.0 * cnt90 / cnt, 1)) + '%',
    }))
