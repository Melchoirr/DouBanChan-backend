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
        media = Media(m_name=m_name, m_type=m_type, m_rate=None, m_rate_num=0, m_heat=0,
                      m_profile_photo=None, m_json=None)
        media.save()
        re['m_id'] = media.m_id
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
        m_id = request.POST['m_id']
        if not Media.objects.filter(m_id=m_id):
            re['msg'] = ERR_MEDIA_NOT_EXISTS
        else:
            media = Media.objects.get(m_id=m_id)
            re['media'] = json.dumps(media, cls=MyEncoder)
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))
