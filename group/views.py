from tools.imports import *


def create_group(request):
    """
    /group/create POST
    create new group
    :param request: g_name g_description
    :return: json, msg = 0, g_id on success
    """
    # 本人加入
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = Group(g_name=request.POST['g_name'],
                      g_description=request.POST['g_description'],
                      g_profile_photo=get_picture_by_id(DEFAULT_PROFILE_PHOTO_ID),
                      g_nickname='人'
                      )
        group.save()
        user_group = UserGroup(user=user, group=group, is_admin=1, is_member=1)
        user_group.save()
        re['msg'] = 0
        re['group'] = group.to_dict()
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def update_group_profile(request):
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = get_group_by_id(request.POST['g_id'])
        user_group = UserGroup.objects.get(user=user, group=group)
        if user_group is not None and user_group.is_admin == 1:  # 这个检查方式ok吗？
            group.g_profile_photo = request.FILES('g_profile_photo')
            group.save()
            re['msg'] = 0
            # 前端进行假修改，无需返回
        else:
            re['msg'] = ERR_NOT_GROUP_ADMIN
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def update_group_description(request):
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = get_group_by_id(request.POST['g_id'])
        user_group = UserGroup.objects.get(user=user, group=group)
        if user_group is not None and user_group.is_admin == 1:  # 这个检查方式ok吗？
            group.g_description = request.POST('g_description')
            group.save()
            re['msg'] = 0
            # 前端进行假修改，无需返回
        else:
            re['msg'] = ERR_NOT_GROUP_ADMIN
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def update_group_tag(request):
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = get_group_by_id(request.POST['g_id'])
        user_group = UserGroup.objects.get(user=user, group=group)
        if user_group is not None and user_group.is_admin == 1:  # 这个检查方式ok吗？
            group.g_profile_photo = request.FILES('g_tag')
            group.save()
            re['msg'] = 0
            # 前端进行假修改，无需返回
        else:
            re['msg'] = ERR_NOT_GROUP_ADMIN
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def update_group_nickname(request):
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = get_group_by_id(request.POST['g_id'])
        user_group = UserGroup.objects.get(user=user, group=group)
        if user_group is not None and user_group.is_admin == 1:  # 这个检查方式ok吗？
            group.g_profile_photo = request.FILES('g_nickname')
            group.save()
            re['msg'] = 0
            # 前端进行假修改，无需返回
        else:
            re['msg'] = ERR_NOT_GROUP_ADMIN
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def delete_group(request):  # 不需要
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


def query_single_group(request):  # post热榜，时间榜，精华帖，给管理员单独页面：处理请求
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
            re['msg'] = 0
            re['group'] = group.to_dict()
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def group_home(request):
    # 按照tag返回
    # 在这里就需要返回有没有加入小组以及是不是管理员，，前端存储下来（仅作为显示之用，其他地方还是要照常判断，比如访问了其他小组的帖子）
    # 返回基础信息
    # 其他的 post之类的另写函数
    return


def join_group(request):  # 这个不需要申请，管理员需要申请
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = get_group_by_id(request.POST['g_id'])
        user_group = UserGroup.objects.get(user=user, group=group)
        if user_group is None:
            new_user_group = UserGroup(user=user, group=group, is_member=1)
            new_user_group.save()
            # 前端把“在小组里”置为1
        else:
            re['msg'] = ERR_ALREADY_JOINED
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def quit_group(request):  # 直接退出
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = get_group_by_id(request.POST['g_id'])
        user_group = UserGroup.objects.get(user=user, group=group)
        user_group.delete()
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def set_essence(request):
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = get_group_by_id(request.POST['g_id'])
        user_group = UserGroup.objects.get(user=user, group=group)
        if user_group is not None and user_group.is_admin == 1:  # 这个检查方式ok吗？
            post = get_post_by_id(request.POST['p_id'])
            post.p_is_essence = 1
            post.save()
            re['msg'] = 0
        else:
            re['msg'] = ERR_NOT_GROUP_ADMIN
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def set_top(request):  # 只修改post详情页返回顺序 ?
    #  ?
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = get_group_by_id(request.POST['g_id'])
        user_group = UserGroup.objects.get(user=user, group=group)
        if user_group is not None and user_group.is_admin == 1:  # 这个检查方式ok吗？
            post = get_post_by_id(request.POST['p_id'])
            post.p_is_top = 1
            post.save()
            re['msg'] = 0
        else:
            re['msg'] = ERR_NOT_GROUP_ADMIN
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def apply_admin(request):  # 和加入小组类似 不需要检查是否加入小组，前端检查
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = get_group_by_id(request.POST['g_id'])
        admin = list(UserGroup.objects.filter(group=group, is_admin=1))
        user_group = UserGroup(user=user, group=group, is_applying=1)
        user_group.save()
        # for each in admin:
        #     message = Message(user=user, admin=admin, a_type=1, a_info=request.POST['a_info'])
        #     message.save()
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def view_apply(request):  #
    # 单独的页面去显示申请
    # 去掉限制之后
    return


def remove_member(request):
    # if agree grant
    # if not delete
    #     send notification?
    return


def grant_admin(request):
    # if agree，加入，均删掉
    return
