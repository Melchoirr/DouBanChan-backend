from tools.imports import *


def query_single_text(request):
    return HttpResponse(json.dumps(_query_single_text(request)))


def _query_single_text(request):
    re = {}
    t_id = request.POST['t_id']
    user = get_cur_user(request)
    text = get_text_by_id(t_id)
    replies = list(Text.objects.filter(t_type=3).filter(t_text=text))
    replies = [x.to_dict() for x in replies]
    replies_sorted_by_time = sorted(replies, key=lambda x: x['t_create_time'].__str__(), reverse=True)
    replies_sorted_by_like = sorted(replies, key=lambda x: x['t_like'], reverse=True)
    re['msg'] = 0
    re['text'] = text.to_dict()
    re['replies_sorted_by_time'] = replies_sorted_by_time
    re['replies_sorted_by_like'] = replies_sorted_by_like
    if user is text.t_user:
        re['is_own'] = 1
    else:
        re['is_own'] = 0
    if text.t_post and text.t_post.p_group:
        if UserGroup.objects.filter(user=user, group=text.t_post.p_group, is_admin=1):
            re['is_group_admin'] = 1
        else:
            re['is_group_admin'] = 0
    else:
        re['is_group_admin'] = 0
    re.update(get_text_status(user, text))
    return re


def get_text_status(user, text):
    re = {
        'is_liked': 0,
        'is_disliked': 0,
        'is_favorite': 0
    }
    if UserText.objects.filter(user=user, text=text, is_liked=1):
        re['is_liked'] = 1
    if UserText.objects.filter(user=user, text=text, is_disliked=1):
        re['is_disliked'] = 1
    if UserText.objects.filter(user=user, text=text, is_favorite=1):
        re['is_favorite'] = 1
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
        applier = get_cur_user(request)
        message = Message(m_applier=applier,
                          m_description='您的评论\'' + text.t_topic + '\'被' + applier.u_name + '评论了',
                          m_user=text.t_user, m_type=2)
        message.save()
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def delete_text(request):
    re = {}
    t_id = request.POST['t_id']
    text = get_text_by_id(t_id)
    text.delete()
    re['msg'] = 0
    return HttpResponse(json.dumps(re))


def cancel_like_text(request):
    re = {}
    if basic_check(request):
        t_id = request.POST['t_id']
        text = get_text_by_id(t_id)
        applier = get_cur_user(request)
        if UserText.objects.filter(user=applier, text=text, is_liked=1):
            text.cancel_like()
        user_text = UserText.objects.get(user=applier, text=text)
        user_text.is_liked = 0
        user_text.save()
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
        text.like()
        if UserText.objects.filter(user=applier, text=text):
            user_text = UserText.objects.get(user=applier, text=text)
            user_text.is_liked = 1
            user_text.save()
        else:
            user_text = UserText(user=applier, text=text, is_liked=1)
            user_text.save()
        # 发信息，
        message = Message(m_applier=applier,
                          m_description='您的评论\'' + text.t_topic + '\'被' + applier.u_name + '点赞了',
                          m_user=text.t_user, m_type=1)
        # 就直接用topic了，空的也不管了
        message.save()
        re['msg'] = 0
        cancel_dislike_text(request)
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def dislike_text(request):
    re = {}
    if basic_check(request):
        t_id = request.POST['t_id']
        text = get_text_by_id(t_id)
        text.dislike()
        applier = get_cur_user(request)
        if UserText.objects.filter(user=applier, text=text):
            user_text = UserText.objects.get(user=applier, text=text)
            user_text.is_disliked = 1
            user_text.save()
        else:
            user_text = UserText(user=applier, text=text, is_disliked=1)
            user_text.save()
        re['msg'] = 0
        cancel_like_text(request)
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def cancel_dislike_text(request):
    re = {}
    if basic_check(request):
        t_id = request.POST['t_id']
        text = get_text_by_id(t_id)
        applier = get_cur_user(request)
        if UserText.objects.filter(user=applier, text=text, is_disliked=1):
            text.cancel_dislike()
        user_text = UserText.objects.get(user=applier, text=text)
        user_text.is_disliked = 0
        user_text.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def text_set_favorite(request):
    user = get_cur_user(request)
    text = get_text_by_id(request.POST['t_id'])
    text.t_favorite += 1
    text.save()
    if UserText.objects.filter(user=user, text=text):
        user_text = UserText.objects.get(user=user, text=text)
        user_text.is_favorite = 1
        user_text.save()
    else:
        user_text = UserText(user=user, text=text, is_favorite=1)
        user_text.save()
    return HttpResponse(json.dumps({}))


def text_cancel_favorite(request):
    user = get_cur_user(request)
    text = get_text_by_id(request.POST['t_id'])
    text.t_favorite -= 1
    text.save()
    user_text = UserText.objects.get(user=user, text=text)
    user_text.is_favorite = 0
    user_text.save()
    return HttpResponse(json.dumps({}))


def is_liked(user, text):
    return UserText.objects.filter(user=user, text=text, is_liked=1)


def is_disliked(user, text):
    return UserText.objects.filter(user=user, text=text, is_disliked=1)


def get_text_replies(text):
    replies = list(Text.objects.filter(t_text=text))
    replies = [x.to_dict() for x in replies]
    replies_by_time = sorted(replies, key=lambda x: x['t_create_time'].__str__(), reverse=True)
    replies_by_like = sorted(replies, key=lambda x: x['t_like'], reverse=True)
    return {
        'replies_by_time': replies_by_time,
        'replies_by_like': replies_by_like
    }
