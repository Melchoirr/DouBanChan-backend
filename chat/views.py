from tools.imports import *


def create_chat(request):  # 检查是否登录
    """
    /chat/create POST
    create new chat
    :param request: c_name c_description
    :return: json, msg = 0, c_id on success
    """
    re = {}
    if basic_check(request):
        default_profile_photo = get_picture_by_id(DEFAULT_PROFILE_PHOTO_ID)
        chat = Chat(c_name=request.POST['c_name'],
                    c_description=request.POST['c_description'],
                    c_profile_photo=default_profile_photo,
                    c_users_num=1,
                    )
        chat.save()
        user_chat = UserChat(user=get_cur_user(request), chat=chat)
        user_chat.save()
        if 'group' in request.POST:
            chat.c_father_group = get_group_by_id(request.POST['group'])
            chat.save()
        # users
        re['msg'] = 0
        re['chat'] = chat.to_dict()
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def delete_chat(request):
    """
    /chat/create POST
    delete media
    :param request: c_id
    :return: json, msg = 0 on success
    """
    re = {}
    if basic_check(request):
        chat_id = request.POST['c_id']
        if not Chat.objects.filter(c_id=chat_id):
            re['msg'] = ERR_CHAT_NOT_EXISTS
        else:
            chat = Chat.objects.get(c_id=chat_id)
            chat.delete()
            re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def query_single_chat(request):
    """
    /chat/query_single POST
    query single chat
    :param request: c_id
    :return: json, msg = 0, chat on success
    """
    re = {}
    if basic_check(request):
        c_id = request.POST['c_id']
        if not Chat.objects.filter(c_id=c_id):
            re['msg'] = ERR_CHAT_NOT_EXISTS
        else:
            chat = Chat.objects.get(c_id=c_id)
            re['msg'] = 0
            re['chat'] = chat.to_dict()
            c_medias = []
            for media in chat.c_medias.all():
                c_medias.append(media.to_dict())
            re['medias'] = c_medias
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def chat_home(request):
    re = {}
    if request.method != 'POST':
        heat_list = []
        heat_set = list(Chat.objects.all().order_by('-c_heat'))[: 10]
        for each in heat_set:
            heat_list.append(each.to_dict())
        re['chat_heat_list'] = heat_list
        post_heat_list = []
        post_heat_set = list(Post.objects.all().order_by('-p_like'))
        for each in post_heat_set:
            post_heat_list.append(each.to_dict())
        re['post_heat_list'] = post_heat_list
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def join_chat(request):  # 前端应该不会调用
    re = {}
    if basic_check(request):
        c_id = request.POST['c_id']
        user = get_cur_user(request)
        chat = get_chat_by_id(c_id)
        if UserChat.objects.filter(user=user, chat=chat):
            re['msg'] = ERR_ALREADY_JOINED
        else:
            chat.c_users_num += 1
            chat.save()
            user_chat = UserChat(user=user, chat=chat)
            user_chat.save()
            re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def quit_chat(request):  # 前端应该不会调用
    re = {}
    if basic_check(request):
        c_id = request.POST['c_id']
        user = get_cur_user(request)
        chat = get_chat_by_id(c_id)
        if UserChat.objects.filter(user=user, chat=chat):
            user_chat = UserChat.objects.get(user=user, chat=chat)
            print(user_chat)
            user_chat.delete()
            re['msg'] = 0
        else:
            chat.c_users_num -= 1
            chat.save()
            re['msg'] = ERR_NOT_JOINED
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def add_post(request):
    re = {}
    if basic_check(request):
        c_id = request.POST['c_id']
        user = get_cur_user(request)
        chat = get_chat_by_id(c_id)
        chat.c_users.add(user)
        chat.c_heat += 1
        chat.save()
        post = Post(p_title=request.POST['p_title'],
                    p_user=user,
                    p_chat=chat,
                    p_floor_num=1)
        text = Text(t_type=2,
                    t_user=user,
                    t_description=request.POST['text'],
                    t_topic=request.POST['topic'],
                    t_floor=1,
                    t_post=post)
        if 'group' in request.POST:
            group = get_group_by_id(request.POST['group'])
            if UserGroup.objects.filter(user=user, group=group):
                post.p_group = group
            else:
                re['msg'] = ERR_NOT_JOINED
                return HttpResponse(json.dumps(re))
        text.save()
        post.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


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


