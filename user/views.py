from io import BytesIO

from django.core.files.base import ContentFile
from django.shortcuts import HttpResponse
from PIL import Image

import json
from django import forms
from models.models import User, Picture
from tools.processing import getPicture
from tools.tools import *


def register(request):
    """
    /user/register POST
    user register
    :param request: username password1 password2 email profile_photo
    :return: json, msg = 0 on success
    """
    re = {}
    if request.method == 'POST':
        name = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        #email = request.POST['email']
        #profile_photo = request.POST['profile_photo']
        if User.objects.filter(u_name=name):
            re['msg'] = ERR_USERNAME_EXISTS
        elif password1 != password2:
            re['msg'] = ERR_PASSWORD_NOT_SAME
        else:
            user = User(u_name=name, u_password=password1)
            user.save()
            re['msg'] = 0
            re['u_id'] = user.u_id
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
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def logout(request):
    """
    /user/logout GET
    user register
    :param request:
    :return: json, msg = 0 on success
    """
    re = {}
    if request.method == 'GET':
        if request.session[CUR_USER_ID] == 0:
            re['msg'] = ERR_NO_CURRENT_USER
        else:
            request.session[CUR_USER_ID] = 0
            re['msg'] = 0

    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def uploadProfile(request):
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

        # with open(picture.p_content.path, 'rb') as f:
        #     image_data = f.read()
        # image = Image.open(BytesIO(image_data))
        #
        # # 定义目标尺寸
        # target_width = 800
        # target_height = 600
        #
        # # 调整尺寸
        # resized_image = image.resize((target_width, target_height), Image.ANTIALIAS)
        # image_content = resized_image.tobytes()
        #
        # # 创建ContentFile并保存到ImageField
        # picture.p_content.save(picture.p_content.url, ContentFile(image_content))
        # find user
        # update this user's profile
        user = User.objects.get(u_id=request.session[CUR_USER_ID])
        user.u_profile_photo = picture
        user.save()
        re['msg'] = 0
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def getUserPage(request):
    re = {}
    if request.method == 'POST':
        u_id = request.session[CUR_USER_ID]
        user = User.objects.get(u_id=u_id)
        u_profile_photo = getPicture(user.u_profile_photo)
        re['u_profile_photo'] = u_profile_photo
        re['u_name'] = user.u_name
        return HttpResponse(json.dumps(re))
    return HttpResponse('Fail')


def getUserBrief(request):
    re = {}
    if request.method == 'POST':
        u_id = request.session[CUR_USER_ID]
        user = User.objects.get(u_id=u_id)
        u_profile_photo = getPicture(user.u_profile_photo)
        re['u_profile_photo'] = u_profile_photo
        re['u_name'] = user.u_name
        return HttpResponse(json.dumps(re))
    return HttpResponse('Fail')