import copy
from tools.imports import *
from tools.tools import *


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
        default_profile_photo = get_picture_by_id(DEFAULT_PROFILE_PHOTO_ID)
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
                        'is_disliked': 0
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
                        'is_disliked': 0
                    })
            re['text_by_time'] = copy.deepcopy(tmp)
            re['text_by_like'] = copy.deepcopy(tmp)
            sorted(re['text_by_time'], key=lambda x: x['text']['t_create_time'])
            sorted(re['text_by_like'], key=lambda x: x['text']['t_like'])
            re['text_by_time'].reverse()
            re['text_by_like'].reverse()
            re['m_chats'] = [x.to_dict() for x in list(media.m_chats)]
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def media_home(request):
    re = {}
    if request.method == 'POST':
        heat_set = list(Media.objects.all().order_by('-m_rate_num')[:10])
        heat_list = []
        for each in heat_set:
            heat_list.append(each.to_dict())
        score_set = list(Media.objects.all().order_by('-m_rate')[:10])
        score_list = []
        for each in score_set:
            score_list.append(each.to_dict())
        re['heat_list'] = heat_list
        re['score_list'] = score_list
        u_id = request.POST['u_id']
        to_be_watched = []
        watching = []
        watched = []
        if User.objects.filter(u_id=u_id):
            user = User.objects.get(u_id=u_id)
            for media in user.u_medias.all():
                user_media = UserMedia.objects.get(media=media, user=user)
                if user_media.is_to_be_watched == 1:
                    to_be_watched.append(media.to_dict())
                if user_media.is_watching == 1:
                    watching.append(media.to_dict())
                if user_media.is_watched == 1:
                    watched.append(media.to_dict())
        re['is_to_be_watched'] = to_be_watched
        re['is_watching'] = watching
        re['is_watched'] = watched
        re['msg'] = 0
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
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

