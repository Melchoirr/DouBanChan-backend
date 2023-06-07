from report.views import *
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
        # g_profile_photo = Picture(p_content=request.FILES['profile'])
        # g_profile_photo.save()
        # g_head_photo = Picture(p_content=request.FILES['head'])
        # g_head_photo.save()
        group = Group(g_name=request.POST['g_name'],
                      g_description=request.POST['g_description'],
                      g_tag=request.POST['g_tag'],
                      g_profile_photo=get_picture_by_id(request.POST['avatar']),
                      g_head_photo=get_picture_by_id(request.POST['head']),
                      g_nickname='人'
                      )
        group.save()
        user_group = UserGroup(user=user, group=group, is_admin=1, is_member=1)
        user_group.save()
        re['msg'] = 0
        # re['group'] = group.to_dict()
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


def update_group_head(request):
    re = {}
    group = get_group_by_id(request.POST['g_id'])
    group.g_profile_photo = request.FILES('g_head_photo')
    group.save()
    return


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
            group.g_profile_photo = request.POST('g_tag')
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
            group.g_profile_photo = request.POST('g_nickname')
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


# def query_single_group(request):  # post热榜，时间榜，精华帖，给管理员单独页面：处理请求
#     """
#     /media/query_single POST
#     query single group
#     :param request: g_id
#     :return: json, msg = 0, group on success
#     """
#     re = {}
#     if request.method == 'POST':
#         g_id = request.POST['g_id']
#         if not Group.objects.filter(g_id=g_id):
#             re['msg'] = ERR_GROUP_NOT_EXISTS
#         else:
#             group = Group.objects.get(g_id=g_id)
#             re['msg'] = 0
#             re['group'] = group.to_dict()
#     else:
#         re['msg'] = ERR_REQUEST_METHOD_WRONG
#     return HttpResponse(json.dumps(re))


def group_brief(request):
    # 按照tag返回
    # 在这里就需要返回有没有加入小组以及是不是管理员，，前端存储下来（仅作为显示之用，其他地方还是要照常判断，比如访问了其他小组的帖子）
    # 返回基础信息
    # 其他的 post之类的另写函数
    re = {}
    group = get_group_by_id(request.POST['g_id'])
    user = get_cur_user(request)
    re = group.to_dict()
    if UserGroup.objects.filter(user=user, group=group):
        re['userInGroup'] = 1
        if UserGroup.objects.get(user=user, group=group).is_admin == 1:
            re['userIsAdmin'] = 1
        else:
            re['userIsAdmin'] = 0
    else:
        re['userIsAdmin'] = 0
    return HttpResponse(json.dumps(re))

# 根据group tag查询group，post
# 根据group tag查询group
# 根据
# post详情页
#


def join_group(request):  # 这个不需要申请，管理员需要申请
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = get_group_by_id(request.POST['g_id'])
        user_group = UserGroup(user=user, group=group)
        user_group.save()

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


def apply_admin(request):  # 和加入小组类似 不需要检查是否加入小组，前端检查
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = get_group_by_id(request.POST['g_id'])
        apply = Message(m_applier=user, m_group=group, m_type=4, m_description=request.POST['text'])
        apply.save()
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def cancel_admin(request):
    re = {}
    if request.method == 'POST':
        user = get_cur_user(request)
        group = get_group_by_id(request.POST['g_id'])
        user_group = UserGroup.objects.get(user=user, group=group)
        user_group.is_admin = 0
        user_group.save()
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def query_apply(request):
    # 单独的页面去显示申请
    # 去掉限制之后
    # 找到所有的message
    re = {}
    apply_list = []
    print(request.POST)
    for each in list(Message.objects.filter(m_type=4, m_group=get_group_by_id(request.POST['g_id']))):
        apply_list.append(each.to_dict_apply())
    re['li'] = apply_list
    return HttpResponse(json.dumps(re))


def remove_member(request):
    # 目前不需要
    return


def grant_apply(request):
    # if agree，加入，均删掉
    re = {}
    print(request.POST)
    apply = get_message_by_id(request.POST['m_id'])
    user = apply.m_applier
    group = apply.m_group
    user_group = UserGroup.objects.get(user=user, group=group)
    user_group.is_admin = 1
    user_group.save()
    # 后端组合字符串：您的发言“xxx”被举报了：取前几个字？ 最好有标题
    message = Message(m_user=user, m_description=group.g_name + '小组：恭喜你成为管理员', m_group=group, m_type=3)
    delete_message(request)
    return HttpResponse(json.dumps(re))


def deny_apply(request):
    re = {}
    apply = get_message_by_id(request.POST['m_id'])
    user = apply.m_applier
    group = apply.m_group
    message = Message(m_user=user, m_description=group.g_name + '小组：申请管理员未通过', m_group=group, m_type=3)
    delete_message(request)
    return HttpResponse(json.dumps(re))


def query_group_by_tag(request):
    re = {}
    user = get_cur_user(request)
    groupList = []
    print(request.POST)
    if request.POST['g_tag'] != '':
        for group in list(Group.objects.filter(g_tag=request.POST['g_tag'])):
            each = group.to_dict()
            if UserGroup.objects.filter(user=user, group=group):
                each['userInGroup'] = 1
                if UserGroup.objects.get(user=user, group=group).is_admin == 1:
                    each['userIsAdmin'] = 1
                else:
                    each['userIsAdmin'] = 0
            else:
                each['userIsAdmin'] = 0
            groupList.append(each)
    else:
        for group in list(Group.objects.all()):
            each = group.to_dict()
            if UserGroup.objects.filter(user=user, group=group):
                each['userInGroup'] = 1
                if UserGroup.objects.get(user=user, group=group).is_admin == 1:
                    each['userIsAdmin'] = 1
                else:
                    each['userIsAdmin'] = 0
            else:
                each['userIsAdmin'] = 0
            groupList.append(each)
    re['groupList'] = groupList
    return HttpResponse(json.dumps(re))


