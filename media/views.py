import copy
from tools.imports import *


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
        m_episode_num = request.POST['m_episode_num']
        m_duration = request.POST['m_duration']
        m_author = request.POST['m_author']
        m_characters = request.POST['m_characters']
        default_profile_photo = get_picture_by_id(DEFAULT_PROFILE_PHOTO_ID)
        media = Media(m_name=m_name, m_type=m_type, m_profile_photo=default_profile_photo, m_genre=m_genre,
                      m_description=m_description, m_year=m_year, m_director=m_director, m_actor=m_actor,
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
            if CUR_USER_ID in request.session:
                for item in text_to_media:
                    tt = {
                        'text': item.to_dict(),
                        'is_liked': 0,
                        'is_disliked': 0
                    }
                    cur_user = User.objects.get(u_id=request.session[CUR_USER_ID])
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
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def media_home(request):
    re = {}
    if request.method == 'POST':
        heat_set = list(Media.objects.all().order_by('-m_heat')[:3])
        heat_list = []
        for each in heat_set:
            heat_list.append(each.to_dict())
        score_set = list(Media.objects.all().order_by('-m_rate')[:3])
        score_list = []
        for each in score_set:
            score_list.append(each.to_dict())
        re['heat_list'] = heat_list
        re['score_list'] = score_list
        #用户相关列表 随机列表？
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))
