from tools.imports import *


def create_group(request):
    """
    /group/create POST
    create new media
    :param request: m_name m_type
    :return: json, msg = 0 on success
    """
    re = {}
    if request.method == 'POST':
        m_name = request.POST['m_name']
        m_type = request.POST['m_type']
        media = Media(m_name=m_name, m_type=m_type, m_rate=None, m_rate_num=0, m_heat=0)
        media.save()
        re['m_id'] = media.m_id
        re['msg'] = 0
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def delete_group(request):
    pass


def query_single_group(request):
    pass
