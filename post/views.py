from tools.imports import *


def query_single_post(request):
    re = {}
    if basic_check(request):
        p_id = request.POST['p_id']
        post = get_post_by_id(p_id)
        text_by_floor = list(Text.objects.filter(t_post=post))
        text_by_floor = sorted(text_by_floor, key=lambda x: x['floor'])
        re['msg'] = 0
        re['post'] = post.to_dict()
        re['text_by_floor'] = text_by_floor
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def like_post(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        post = request.POST['p_id']
        post.p_like += 1
        post.save()
        user_post = UserPost(post=post, user=user, is_liked=1)
        user_post.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


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
            t_floor=request.POST['t_floor']
        )
        text.save()
        re['msg'] = 0
        re['text'] = text.to_dict()
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))
