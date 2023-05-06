from django.shortcuts import HttpResponse
import json
from models.models import User
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
        email = request.POST['email']
        profile_photo = request.POST['profile_photo']
        if User.objects.filter(u_name=name):
            re['msg'] = ERR_USERNAME_EXISTS
        elif password1 != password2:
            re['msg'] = ERR_PASSWORD_NOT_SAME
        else:
            user = User(u_name=name, u_password=password1, u_prifole_photo=profile_photo, u_email=email)
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
