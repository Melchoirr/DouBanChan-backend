from tools.imports import *


def query_single_post(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        p_id = request.POST['p_id']
        post = get_post_by_id(p_id)
        text_by_floor = list(Text.objects.filter(t_post=post))
        text_by_floor = sorted(text_by_floor, key=lambda x: x['floor'])
        re['msg'] = 0
        re['post'] = post.to_dict()
        re['text_by_floor'] = text_by_floor
        if user is post.p_user:
            re['is_own'] = 1
        else:
            re['is_own'] = 0
        if post.p_group:
            if UserGroup.objects.filter(user=user, group=post.p_group, is_admin=1):
                re['is_group_admin'] = 1
            else:
                re['is_group_admin'] = 0
        else:
            re['is_group_admin'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def like_post(request):
    re = {}
    if basic_check(request):
        applier = get_cur_user(request)
        post = request.POST['p_id']
        post.p_like += 1
        post.save()
        user_post = UserPost(post=post, user=applier, is_liked=1)
        user_post.save()
        # 发信息，
        message = Message(m_applier=applier, m_description='您的帖子\'' + post.p_title + '\'被' + applier.u_name + '点赞了', m_user=post.p_user, m_type=1)
        message.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def post_set_favorite(request):
    user = get_cur_user(request)
    post = request.POST['p_id']
    user_post = UserPost(post=post, user=user, is_favorite=1)
    user_post.save()


def dislike_post(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        post = request.POST['p_id']
        post.p_dislike += 1
        post.save()
        user_post = UserPost(post=post, user=user, is_disliked=1)
        user_post.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def add_text(request):
    re = {}
    if basic_check(request):
        text = Text(
            t_type=2,
            t_user=get_cur_user(request),
            t_description=request.POST['t_description'],
            t_topic=request.POST['t_topic'],
            t_post=get_post_by_id(request.POST['t_post_id']),
            t_floor=request.POST['t_floor']  # 自增
        )
        text.save()
        re['msg'] = 0
        re['text'] = text.to_dict()
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))
