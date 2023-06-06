from tools.imports import *


def add_report(request):  # 或者发布到一个特定区域，直邮管理员有权限访问
    # 发两份
    re = {}
    if basic_check(request):
        report = Message(
            r_user=get_cur_user(request),
            r_text=get_text_by_id(request.POST['t_id']),
            r_details=request.POST['r_details']
        )
        report.save()
        re['msg'] = 0
        re['report'] = report.to_dict()
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def delete_message(request):
    message = get_message_by_id(request.POST['m_id'])
    message.delete()


def query_report(request):
    # 判断是什么管理员
    # 是小组管理员就发g_id
    re = {}
    report_list = []
    if 'g_id' in request.POST:
        group = get_group_by_id(request.POST['g_id'])
        for each in list(Message.objects.filter(m_type=5, m_group=group)):
            report_list.append(each.to_dict())
    else:
        for each in list(Message.objects.filter(m_type=5)):
            report_list.append(each.to_dict())
    re['report_list'] = report_list
    return HttpResponse(json.dumps(re))


def query_single_report(request):  # 好像不一定有详情页
    re = {}
    if basic_check(request):
        report = get_message_by_id(request.POST['r_id'])
        re['msg'] = 0
        re['report'] = report.to_dict()
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))



