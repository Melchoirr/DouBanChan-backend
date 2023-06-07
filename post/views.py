import string

from tools.imports import *


def add_post(request):
    re = {}
    if basic_check(request):
        c_id = request.POST['topicId']
        user = get_cur_user(request)
        chat = get_chat_by_id(c_id)
        chat.c_users.add(user)
        chat.c_heat += 1
        chat.save()
        print(request.POST)
        post = Post(p_title=request.POST['title'],
                    p_user=user,
                    p_chat=chat,
                    p_floor_num=1,
                    p_tag=chat.c_tag)
        post.save()
        text = Text(t_type=2,
                    t_user=user,
                    t_description=request.POST['text'],
                    t_floor=1,
                    t_post=post)
        text.save()
        if 'g_id' in request.POST:
            print("hihihi")
            group = get_group_by_id(request.POST['g_id'])
            post.p_group = group
            chat.c_father_group = group
        if 'picture_list' in request.POST:
            picture_string = request.POST['picture_list']
            picture_list = picture_string.split(',')
            picture_list = [int(x) for x in picture_list]
            for p_id in picture_list:
                print(p_id)
                picture = get_picture_by_id(p_id)
                picture.p_father_text = text
                picture.save()
        post.save()
        chat.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


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
            re['userIsLz'] = 1
        else:
            re['userIsLz'] = 0
        if post.p_group:
            if UserGroup.objects.filter(user=user, group=post.p_group, is_admin=1):
                re['userIsAdmin'] = 1
            else:
                re['userIsAdmin'] = 0
        else:
            re['userIsAdmin'] = 0
        if UserPost.objects.filter(user=user, post=post, is_liked=1):
            re['userLike'] = 1
        else:
            re['userLike'] = 0
        if UserPost.objects.filter(user=user, post=post, is_disliked=1):
            re['userDislike'] = 1
        else:
            re['userDislike'] = 0
        if UserPost.objects.filter(user=user, post=post, is_favorite=1):
            re['userFav'] = 1
        else:
            re['userFav'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_post_status(user, post, group):
    re = {
        'userLike': 0,
        'userDislike': 0,
        'userFav': 0,
        'userIsAdmin': 0,
        'userIsLz': 0,
    }
    if UserPost.objects.filter(user=user, post=post, is_liked=1):
        re['userLike'] = 1
    if UserPost.objects.filter(user=user, post=post, is_disliked=1):
        re['userDislike'] = 1
    if UserPost.objects.filter(user=user, post=post, is_favorite=1):
        re['userFav'] = 1

    if UserGroup.objects.filter(user=user, group=group, is_admin=1):
        re['userIsAdmin'] = 1
    if post.p_user == user:
        re['userIsLz'] = 1
    return re


def get_text_status(user, text):
    re = {
        'userLike': 0,
        'userDislike': 0,
        'userFav': 0,
        'userIsAdmin': 0,
        'userIsLz': 0,
    }
    if UserText.objects.filter(user=user, text=text, is_liked=1):
        re['is_liked'] = 1
    if UserText.objects.filter(user=user, text=text, is_disliked=1):
        re['is_disliked'] = 1
    if UserText.objects.filter(user=user, text=text, is_favorite=1):
        re['is_favorite'] = 1
    return re


def like_post(request):
    re = {}
    if basic_check(request):
        applier = get_cur_user(request)
        post = request.POST['p_id']
        post.p_like += 1
        post.save()
        if UserPost.objects.filter(user=applier, post=post):
            user_post = UserPost.objects.get(user=applier, post=post)
            user_post.is_liked = 1
            user_post.save()
        else:
            user_text = UserText(user=applier, post=post, is_liked=1)
            user_text.save()
        # 发信息，
        message = Message(m_applier=applier, m_description='您的帖子\'' + post.p_title + '\'被' + applier.u_name + '点赞了', m_user=post.p_user, m_type=1)
        message.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def cancel_like_post(request):
    re = {}
    if basic_check(request):
        p_id = request.POST['p_id']
        post = get_post_by_id(p_id)
        post.cancel_like()
        applier = get_cur_user(request)
        user_post = UserPost.objects.get(user=applier, post=post)
        user_post.is_liked = 0
        user_post.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def post_set_favorite(request):
    user = get_cur_user(request)
    post = get_post_by_id(request.POST['t_id'])
    post.t_favorite += 1
    post.save()
    if UserPost.objects.filter(user=user, post=post):
        user_post = UserPost.objects.get(user=user, post=post)
        user_post.is_favorite = 1
        user_post.save()
    else:
        user_post = UserPost(user=user, post=post, is_favorite=1)
        user_post.save()
    return HttpResponse(json.dumps({}))


def post_cancel_favorite(request):
    user = get_cur_user(request)
    post = get_post_by_id(request.POST['p_id'])
    post.p_favorite -= 1
    post.save()
    user_post = UserPost.objects.get(user=user, post=post)
    user_post.is_favorite = 0
    user_post.save()
    return HttpResponse(json.dumps({}))


def dislike_post(request):
    user = get_cur_user(request)
    post = get_post_by_id(request.POST['p_id'])
    post.p_dislike += 1
    post.save()
    if UserPost.objects.filter(user=user, post=post):
        user_post = UserPost.objects.get(user=user, post=post)
        user_post.is_dislike = 1
        user_post.save()
    else:
        user_post = UserPost(user=user, post=post, is_dislike=1)
        user_post.save()
    return HttpResponse(json.dumps({}))


def cancel_dislike_post(request):
    user = get_cur_user(request)
    post = get_post_by_id(request.POST['p_id'])
    post.t_dislike -= 1
    post.save()
    user_post = UserPost.objects.get(user=user, post=post)
    user_post.is_dislike = 0
    user_post.save()
    return HttpResponse(json.dumps({}))
# def add_text(request):
#     re = {}
#     if basic_check(request):
#         text = Text(
#             t_type=2,
#             t_user=get_cur_user(request),
#             t_description=request.POST['t_description'],
#             t_topic=request.POST['t_topic'],
#             t_post=get_post_by_id(request.POST['t_post_id']),
#             t_floor=request.POST['t_floor']  # 自增
#         )
#         text.save()
#         re['msg'] = 0
#         re['text'] = text.to_dict()
#     else:
#         re['msg'] = ERR_OTHER
#     return HttpResponse(json.dumps(re))


def reply_post(request):
    re = {}
    if basic_check(request):
        c_id = request.POST['c_id']
        user = get_cur_user(request)
        chat = get_chat_by_id(c_id)
        chat.c_users.add(user)
        chat.c_heat += 1
        chat.save()
        p_id = request.POST['p_id']
        post = get_post_by_id(p_id)
        text = Text(t_type=2,
                    t_user=user,
                    t_description=request.POST['text'],
                    t_floor=post.p_floor_num + 1,
                    t_post=post)
        if 'group' in request.POST:
            group = get_group_by_id(request.POST['group'])
            if UserGroup.objects.filter(user=user, group=group):
                post.p_group = group
            else:
                re['msg'] = ERR_NOT_JOINED
                return HttpResponse(json.dumps(re))
        post.p_floor_num += 1
        post.save()
        text.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def delete_post(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        p_id = request.POST['p_id']
        post = get_post_by_id(p_id)
        if post.p_user == user:
            post.delete()
        else:
            re['msg'] = ERR_NOT_POSSESSION
            return HttpResponse(json.dumps(re))
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def query_group_posts(request):
    re = {}
    if basic_check(request):
        group = get_group_by_id(request.POST['g_id'])
        user = get_cur_user(request)
        postList = []
        for x in list(Post.objects.filter(p_group=group)):
            post = x.to_dict()
            post.update(get_post_status(user, x, group))
            postList.append(post)
        re['msg'] = 0
        re['postList'] = postList
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def query_chat_posts(request):
    re = {}
    if basic_check(request):
        chat = get_chat_by_id(request.POST['c_id'])
        postList = [x.to_dict() for x in list(Post.objects.filter(p_chat=chat))]
        re['msg'] = 0
        re['postList'] = postList
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def query_posts_by_tag(request):
    re = {}
    if basic_check(request):
        postList = [x.to_dict() for x in list(Post.objects.filter(p_tag=request.POST['p_tag']))]
        re['msg'] = 0
        re['postList'] = postList
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))
