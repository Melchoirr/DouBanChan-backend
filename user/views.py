from django.shortcuts import HttpResponse
import json
from models.models import User, Picture
from tools.tools import *
from tools.imports import *
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
            user = User(u_name=username, u_password=password, u_profile_photo=default_profile_photo, u_email='')
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
            else:
                re['msg'] = 0
                request.session[CUR_USER_ID] = user.u_id
                re['user'] = user.to_dict()
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def logout(request):  # 弃用，前端自己把u_id改成0
    """
    /user/logout POST
    user register
    :param request:
    :return: json, msg = 0 on success
    """
    re = {}
    if request.method == 'POST':
        if CUR_USER_ID not in request.session:
            re['msg'] = ERR_NO_CURRENT_USER
        else:
            request.session[CUR_USER_ID] = -1
            re['msg'] = 0
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


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
            re['groups'] = [group.to_dict() for group in user.u_groups.all()]
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
