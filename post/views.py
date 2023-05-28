from django.shortcuts import render
from tools.imports import *


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



