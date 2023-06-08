from post.views import delete_post
from tools.imports import *


def report_post(request):  # 或者发布到一个特定区域，直邮管理员有权限访问
    # 发两份
    re = {}
    report = Message(
        m_applier=get_cur_user(request),
        m_post=get_post_by_id(request.POST['p_id']),
        m_title=request.POST['m_title'],
        m_description=request.POST['m_description'],
        m_type=5
    )
    report.save()
    re['msg'] = 0
    return HttpResponse(json.dumps(re))


def report_text(request):  # 或者发布到一个特定区域，直邮管理员有权限访问
    # 发两份
    re = {}
    report = Message(
        m_applier=get_cur_user(request),
        m_text=get_text_by_id(request.POST['t_id']),
        m_title=request.POST['m_title'],
        m_description=request.POST['m_description'],
        m_type=5
    )
    report.save()
    re['msg'] = 0
    return HttpResponse(json.dumps(re))


def query_report(request):
    re = {}
    user = get_cur_user(request)
    print(request.POST)
    if user.u_authority == 1:
        re['report_list'] = [x.to_dict_report_post() for x in list(Message.objects.filter(m_type=5))]
    return HttpResponse(json.dumps(re))


def handle_report_post(request):
    re = {}
    handle = request.POST['handle']

    report = Message.objects.get(m_id=request.POST['id'])
    print(request.POST)
    if handle == '1':
        report.m_is_handled = 1
        if Post.objects.filter(p_id=request.POST['p_id']):
            post = get_post_by_id(request.POST['p_id'])
            message = Message(m_title='您的评论违规，已被管理员删除', m_description='您的帖子\'' + post.p_title + '\'已被管理员删除',
                              m_user=post.p_user, m_type=3)
            message.save()
            report.delete()
            post.delete()

    if handle == '2':
        report.m_is_handled = 2
        report.save()
    return HttpResponse(json.dumps(re))


def query_system_message(request):
    re = {}
    user = get_cur_user(request)
    print(request.POST)
    re['system_message_list'] = [x.to_dict_system() for x in list(Message.objects.filter(m_type=3, m_user=user))]
    return HttpResponse(json.dumps(re))


def query_like_message(request):
    re = {}
    user = get_cur_user(request)
    print(request.POST)
    re['system_message_list'] = [x.to_dict_system() for x in list(Message.objects.filter(m_type=3, m_user=user))]
    return HttpResponse(json.dumps(re))


def delete_message(request):
    re = {}
    message = Message.objects.get(m_id=request.POST['m_id'])
    message.delete()
    return HttpResponse(json.dumps(re))


def query_comment_message(request):
    re = {}
    user = get_cur_user(request)
    print(request.POST)
    re['comment_message_list'] = [x.to_dict_comment() for x in list(Message.objects.filter(m_type=2, m_user=user))]
    return HttpResponse(json.dumps(re))


# def query_report(request):
#     # 判断是什么管理员
#     # 是小组管理员就发g_id
#     re = {}
#     report_list = []
#     if 'g_id' in request.POST:
#         group = get_group_by_id(request.POST['g_id'])
#         for each in list(Message.objects.filter(m_type=5, m_group=group)):
#             report_list.append(each.to_dict())
#     else:
#         for each in list(Message.objects.filter(m_type=5)):
#             report_list.append(each.to_dict())
#     re['report_list'] = report_list
#     return HttpResponse(json.dumps(re))


def query_single_report(request):  # 好像不一定有详情页
    re = {}
    if basic_check(request):
        report = get_message_by_id(request.POST['r_id'])
        re['msg'] = 0
        re['report'] = report.to_dict()
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))



