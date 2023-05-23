from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import HttpResponse
from PIL import Image

import json
from django import forms
from models.models import User, Picture, Text
from tools.tools import *


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
        if User.objects.filter(u_name=username):
            re['msg'] = ERR_USERNAME_EXISTS
        else:
            user = User(u_name=username, u_password=password)
            user.save()
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
        if CUR_USER_ID not in request.session:
            re['msg'] = ERR_NO_CURRENT_USER
        else:
            request.session[CUR_USER_ID] = -1
            re['msg'] = 0

    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def chage_password(request):
    return

def upload_profile(request):
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


def get_user_page(request):
    re = {}
    if request.method == 'POST':
        u_id = request.session[CUR_USER_ID]
        user = User.objects.get(u_id=u_id)
        re['user'] = user.to_dict()
        re['msg'] = 0
        return HttpResponse(json.dumps(re))
    re['msg'] = 1
    return HttpResponse(json.dumps(re))


def get_user_brief(request):
    re = {}
    if request.method == 'POST':
        u_id = request.session[CUR_USER_ID]
        user = User.objects.get(u_id=u_id)
        re['user'] = user.to_dict()
        re['msg'] = 0
        return HttpResponse(json.dumps(re))
    re['msg'] = 1
    return HttpResponse(json.dumps(re))
