import copy
from tools.imports import *
from tools.tools import *
from text.views import get_text_replies


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
            sorted(re['text_by_time'], key=lambda x: x['text']['t_create_time'], reverse=True)
            sorted(re['text_by_like'], key=lambda x: x['text']['t_like'], reverse=True)
            re['m_chats'] = [x.to_dict() for x in list(media.m_chats.all())]
            re['m_preview'] = get_media_preview(m_id)
            re['rate'] = get_user_rate(user, media)
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def get_user_rate(user, media):
    if UserMedia.objects.filter(user=user, media=media):
        um = UserMedia.objects.get(user=user, media=media)
        return um.rate
    return 0


def get_media_preview(m_id):
    media = get_media_by_id(m_id)
    previews = list(Picture.objects.filter(p_media=media))
    return [x.to_dict() for x in previews]


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
        comments = list(Text.objects.filter(t_type=1))[:10]
        comments = [x.to_dict() for x in comments]
        re['msg'] = 0
        re['heat_comment'] = comments
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def heated_movie(request):
    re = {}
    if basic_check(request):
        _heated_movie = list(Media.objects.filter(m_type=1))[:10]
        _heated_movie = [x.to_dict() for x in _heated_movie]
        _heated_movie = sorted(_heated_movie, key=lambda x: x['m_heat'], reverse=True)
        ##############################################
        print(_heated_movie)
        ##############################################
        re['msg'] = 0
        re['heat_movie'] = _heated_movie
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def heated_series(request):
    re = {}
    if basic_check(request):
        _heated_series = list(Media.objects.filter(m_type=2))[:10]
        _heated_series = [x.to_dict() for x in _heated_series]
        _heated_series = sorted(_heated_series, key=lambda x: x['m_heat'], reverse=True)
        re['msg'] = 0
        re['heat_series'] = _heated_series
    else:
        re['msg'] = ERR_OTHER
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
        media = Media.objects.get(m_id=m_id)
        media.m_rate = (media.m_rate * media.m_rate_num + float(request.POST['t_rate'])) / (media.m_rate_num + 1)
        media.m_rate_num += 1
        media.save()
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

