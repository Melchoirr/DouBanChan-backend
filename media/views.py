from django.http import JsonResponse

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
        media = Media(m_name=m_name, m_type=m_type)
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
        m_id = request.POST.get('m_id')
        if not Media.objects.filter(m_id=m_id):
            re['msg'] = ERR_MEDIA_NOT_EXISTS
        else:
            media = Media.objects.get(m_id=m_id)
            media.m_heat += 1
            media.save()
            re['msg'] = 0
            re['media'] = media.to_dict()
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
