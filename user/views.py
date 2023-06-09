from sender.views import *


def register(request):
    """
    /user/register POST
    user register
    :param request: username password
    :return: json, msg = 0 on success
    """
    re = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(u_name=username):
            re['msg'] = ERR_USERNAME_EXISTS
        else:
            default_profile_photo = get_picture_by_id(DEFAULT_PROFILE_PHOTO_ID)
            user = User(u_name=username, u_password=password, u_profile_photo=default_profile_photo, u_email=email, u_nickname=username)
            user.save()
            ###############################################
            send_email(email, user.u_id)
            ###############################################
            re['msg'] = 0
            re['user'] = user.to_dict()
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def login(request):
    """
    /user/login POST
    user register
    :param request: username password
    :return: json, msg = 0 on success
    """
    re = {}
    if request.method == 'POST':
        u_name = request.POST['username']
        u_password = request.POST['password']
        if not User.objects.filter(u_name=u_name):
            re['msg'] = ERR_USER_NOT_EXISTS
        else:
            user = User.objects.get(u_name=u_name)
            if u_password != user.u_password:
                re['msg'] = ERR_PASSWORD_WRONG
            elif not user.is_active:
                re['msg'] = ERR_USER_NOT_ACTIVE
            else:
                re['msg'] = 0
                request.session[CUR_USER_ID] = user.u_id
                re['user'] = user.to_dict()
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


# def logout(request):  # 弃用，前端自己把u_id改成1
#     """
#     /user/logout POST
#     user register
#     :param request:
#     :return: json, msg = 0 on success
#     """
#     re = {}
#     if request.method == 'POST':
#         if CUR_USER_ID not in request.session:
#             re['msg'] = ERR_NO_CURRENT_USER
#         else:
#             request.session[CUR_USER_ID] = -1
#             re['msg'] = 0
#     else:
#         re['msg'] = ERR_REQUEST_METHOD_WRONG
#     return HttpResponse(json.dumps(re))


def query_single_user(request):
    re = {}
    if request.method == 'POST':
        u_id = request.POST['u_id']
        if User.objects.filter(u_id=u_id):
            user = User.objects.get(u_id=u_id)
            re['msg'] = 0
            re['user'] = user.to_dict()
            collection = []
            for media in user.u_medias.all():
                user_media = UserMedia.objects.get(media=media, user=user)
                if user_media.is_in_collection == 1:
                    collection.append(media.to_dict())
            re['collection'] = collection
            re['groupList'] = [group.to_dict() for group in user.u_groups.all()]
            re['chat'] = [chat.to_dict() for chat in user.u_chats.all()]
        else:
            re['msg'] = ERR_USER_NOT_EXISTS
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def update_password(request):
    re = {}
    if request.method == 'POST':
        user = User.objects.get(u_id=request.POST['u_id'])
        user.u_password = request.POST['new_password']
        user.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def update_email(request):
    re = {}
    if request.method == 'POST':
        user = User.objects.get(u_id=request.POST['u_id'])
        user.u_email = request.POST['new_email']
        user.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def update_profile(request):
    """

    :param request:
    :return:
    三个地方需要用到上传图片
    """
    re = {}
    if request.method == 'POST':
        p_content = request.FILES['p_content']
        picture = Picture(p_content=p_content)
        picture.save()
        user = User.objects.get(u_id=request.POST['u_id'])
        user.u_profile_photo = picture
        user.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def get_user_movie(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        ums = list(UserMedia.objects.filter(user=user, is_in_collection=1, media__m_type=1))
        movies = [x.media.to_dict() for x in ums]
        re['msg'] = 0
        re['movies'] = movies
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_user_series(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        ums = list(UserMedia.objects.filter(user=user, is_in_collection=1, media__m_type=2))
        movies = [x.media.to_dict() for x in ums]
        re['msg'] = 0
        re['series'] = movies
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_user_book(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        ums = list(UserMedia.objects.filter(user=user, is_in_collection=1, media__m_type=3))
        movies = [x.media.to_dict() for x in ums]
        re['msg'] = 0
        re['books'] = movies
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_user_fav_post(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        ups = list(UserPost.objects.filter(user=user, is_favorite=1))
        posts = [x.post.to_dict() for x in ups]
        re['msg'] = 0
        re['posts'] = posts
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_user_fav_text(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        ups = list(UserText.objects.filter(user=user, is_favorite=1))
        posts = [x.text.to_dict() for x in ups]
        re['msg'] = 0
        re['texts'] = posts
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_self_post(request):
    re = {}
    print(request.POST)
    if basic_check(request):
        user = get_cur_user(request)
        posts = list(Post.objects.filter(p_user=user))
        posts = [x.to_dict() for x in posts]
        re['msg'] = 0
        re['posts'] = posts
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_self_group(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        ugs = list(UserGroup.objects.filter(user=user))
        groups = [x.group.to_dict() for x in ugs]
        re['msg'] = 0
        re['groups'] = groups
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def get_self_chat(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        ucs = list(UserChat.objects.filter(user=user))
        chats = [x.chat.to_dict() for x in ucs]
        re['msg'] = 0
        re['chats'] = chats
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def change_profile(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        user.u_nickname = request.POST['u_nickname']
        user.u_gender = request.POST['u_gender']
        user.u_birthday = request.POST['u_birthday']
        user.u_signature = request.POST['u_signature']
        user.u_desc = request.POST['u_desc']
        user.save()
        re['msg'] = 0
        re['user'] = user.to_dict()
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def change_password(request):
    re = {}
    if basic_check(request):
        user = get_cur_user(request)
        new_password = request.POST['new_password']
        user.u_password = new_password
        user.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_OTHER
    return HttpResponse(json.dumps(re))


def user_collection_media(request):
    print(request.POST)
    user = get_cur_user(request)
    ums = list(UserMedia.objects.filter(user=user, is_in_collection=1))
    re = []
    for um in ums:
        re.append(um.media.to_dict())
    return HttpResponse(json.dumps(re))


