from tools.imports import *


def create_group(request):
    """
    /group/create POST
    create new group
    :param request: g_name g_description
    :return: json, msg = 0, g_id on success
    """
    re = {}
    if request.method == 'POST':
        g_name = request.POST['g_name']
        g_description = request.POST['g_description']
        new_group = Group(g_name=g_name, g_description=g_description,
                          g_create_time=timezone.now(), g_last_modify_time=timezone.now())
        new_group.save()
        re['msg'] = 0
        re['g_id'] = new_group.g_id
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def delete_group(request):
    """
    /group/delete POST
    delete group
    :param request: g_id
    :return: json, msg = 0 on success
    """
    re = {}
    if request.method == 'POST':
        group_id = request.POST['g_id']
        if not Group.objects.filter(g_id=group_id):
            re['msg'] = ERR_GROUP_NOT_EXISTS
        else:
            group = Group.objects.get(m_id=group_id)
            group.delete()
            re['msg'] = 0
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def query_single_group(request):
    """
    /media/query_single POST
    query single group
    :param request: g_id
    :return: json, msg = 0, group on success
    """
    re = {}
    if request.method == 'POST':
        g_id = request.POST['g_id']
        if not Group.objects.filter(g_id=g_id):
            re['msg'] = ERR_GROUP_NOT_EXISTS
        else:
            group = Group.objects.get(g_id=g_id)
            re['group'] = json.dumps(group, cls=MyEncoder)
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))
