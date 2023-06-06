import difflib

from tools.imports import *


def query_base(request):
    re = {}
    if request.method == 'POST':
        re_user = _query_user(request)
        re_chat = _query_chat(request)
        re_group = _query_group(request)
        re_media = _query_media(request)
        re_report = _query_report(request)
        re = {
            'msg': 0,
            'data': {
                'user': re_user,
                'chat': re_chat,
                'group': re_group,
                'media': re_media,
                'report': re_report
            }
        }
    else:
        re = {'msg': ERR_REQUEST_METHOD_WRONG}
    return HttpResponse(json.dumps(re))


def query_user(request):
    return HttpResponse(json.dumps(_query_user(request)))


def _query_user(request):
    re = {}
    if request.method == 'POST':
        qstr = request.POST['qstr']
        data = User.objects.filter(u_name__icontains=qstr)
        data = sorted(data, key=lambda x: weight(qstr, x.u_name))
        re['msg'] = 0
        result = []
        for item in data:
            result.append(item.to_dict())
        re['data'] = result
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return re


def query_chat(request):
    return HttpResponse(json.dumps(_query_chat(request)))


def _query_chat(request):
    re = {}
    if request.method == 'POST':
        qstr = request.POST['qstr']
        data = Chat.objects.filter(Q(c_name__icontains=qstr) or Q(c_description__icontains=qstr))
        data = sorted(data, key=lambda x: weight(qstr, x.c_name + x.c_description))
        re['msg'] = 0
        result = []
        for item in data:
            result.append(item.to_dict())
        re['data'] = result
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return re


def query_group(request):
    return HttpResponse(json.dumps(_query_group(request)))


def _query_group(request):
    re = {}
    if request.method == 'POST':
        qstr = request.POST['qstr']
        data = Group.objects.filter(Q(g_name__icontains=qstr) or
                                    Q(g_description__icontains=qstr) or
                                    Q(g_tag__icontains=qstr))
        data = sorted(data, key=lambda x: weight(qstr, x.g_name + x.g_description))
        re['msg'] = 0
        result = []
        for item in data:
            result.append(item.to_dict())
        re['data'] = result
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return re


def query_media(request):
    return HttpResponse(json.dumps(_query_media(request)))


def _query_media(request):
    re = {}
    if request.method == 'POST':
        qstr = request.POST['qstr']
        data = Media.objects.filter(Q(m_name__icontains=qstr) or Q(m_description__icontains=qstr)
                                    or Q(m_genre__icontains=qstr) or Q(m_region__icontains=qstr)
                                    or Q(m_director__icontains=qstr) or Q(m_actor__icontains=qstr)
                                    or Q(m_author__icontains=qstr))
        data = sorted(data, key=lambda x: weight(qstr, x.m_name + x.m_description + x.m_genre
                                                 + x.m_region + x.m_director + x.m_actor + x.m_author))
        re['msg'] = 0
        result = []
        for item in data:
            result.append(item.to_dict())
        re['data'] = result
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return re


def query_report(request):
    return HttpResponse(json.dumps(_query_report(request)))


def _query_report(request):
    re = {}
    if request.method == 'POST':
        qstr = request.POST['qstr']
        data = Report.objects.filter(r_details__icontains=qstr)
        data = sorted(data, key=lambda x: weight(qstr, x.r_details))
        re['msg'] = 0
        result = []
        for item in data:
            result.append(item.to_dict())
        re['data'] = result
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return re


def weight(str1, str2):
    seq_matcher = difflib.SequenceMatcher(None, str1, str2)
    return round(seq_matcher.ratio() * max(len(str1), len(str2)))
