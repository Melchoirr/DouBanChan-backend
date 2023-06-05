from tools.imports import *


def add_report(request):  # 或者发布到一个特定区域，直邮管理员有权限访问
    re = {}
    if basic_check(request):
        report = Report(
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


def delete_report(request):
    re = {}
    if basic_check(request):
        report = get_report_by_id(request.POST['r_id'])
        report.delete()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def query_single_report(request):
    re = {}
    if basic_check(request):
        report = get_report_by_id(request.POST['r_id'])
        re['msg'] = 0
        re['report'] = report.to_dict()
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))
