from tools.imports import *


def query_single_text(request):
    t_id = request.POST['t_id']
    return HttpResponse(json.dumps(_query_single_text(t_id)))


def _query_single_text(t_id):
    re = {}
    text = get_text_by_id(t_id)
    replies = list(Text.objects.filter(t_type=3).filter(t_text=text))
    replies = [x.to_dict() for x in replies]
    replies_sorted_by_time = sorted(replies, key=lambda x: x['t_create_time'].__str__())
    replies_sorted_by_like = sorted(replies, key=lambda x: x['t_like'])
    re['msg'] = 0
    re['text'] = text.to_dict()
    re['replies_sorted_by_time'] = replies_sorted_by_time
    re['replies_sorted_by_like'] = replies_sorted_by_like
    return re


def reply_text(request):
    re = {}
    if basic_check(request):
        text = Text(
            t_type=3,
            t_user=get_cur_user(request),
            t_description=request.POST['t_description'],
            t_text=get_text_by_id(request.POST['t_father_text_id'])
        )
        text.save()
        re['msg'] = 0
        re['text'] = text.to_dict()
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def delete_text(request):
    re = {}
    if basic_check(request):
        t_id = request.POST['t_id']
        text = get_text_by_id(t_id)
        text.delete()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def like_text(request):
    re = {}
    if basic_check(request):
        t_id = request.POST['t_id']
        text = get_text_by_id(t_id)
        applier = get_cur_user(request)
        if not is_liked(applier, text):
            text.like()
            # 发信息，
            message = Message(m_applier=applier,
                              m_description='您的评论\'' + text.t_topic + '\'被' + applier.u_name + '点赞了',
                              m_user=text.t_user, m_type=1)
            # 就直接用topic了，空的也不管了
            message.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def dislike_text(request):
    re = {}
    if basic_check(request):
        t_id = request.POST['t_id']
        text = get_text_by_id(t_id)
        if not is_disliked(get_cur_user(request), text):
            text.dislike()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def is_liked(user, text):
    return UserText.objects.filter(user=user, text=text, is_liked=1)


def is_disliked(user, text):
    return UserText.objects.filter(user=user, text=text, is_disliked=1)
