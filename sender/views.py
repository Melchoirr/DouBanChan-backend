import os
import platform
import random
from random import Random
from django.core.mail import EmailMessage
from django.db.models import *
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from tools.imports import *
from DouBanChan_Backend.settings import EMAIL_HOST_USER


def send_email(email, u_id):
    # 验证路由
    # url = jwt.encode(token, SECRET_KEY, algorithm='HS256')  # 加密生成字符串
    url = '' + str(u_id)
    if platform.system() == "Linux":
        url = os.path.join("https://milimili.super2021.com:8000/sender/activate/", url)
    else:
        url = os.path.join("http://127.0.0.1:8000/sender/activate/", url)
    data = {'url': url}
    email_title = r"欢迎注册MiliMili短视频分享平台"
    email_body = loader.render_to_string('EmailContent-register.html', data)
    msg = EmailMessage(email_title, email_body, EMAIL_HOST_USER, [email])
    msg.content_subtype = 'html'
    send_status = msg.send()
    return send_status


def activate(request, u_id):
    try:
        user = User.objects.get(u_id=u_id)
        user.is_active = True
        user.save()
        data = {"title": "感谢注册", "message": "注册豆瓣酱图书影视交流平台成功！", "url": "http://127.0.0.1:8000/"}
        return render(request, 'EmailContent-check.html', data)
    except Exception:
        data = {"title": "注册失败", "message": "注册豆瓣酱图书影视交流平台失败！", "url": "http://127.0.0.1:8000/"}
        return render(request, 'EmailContent-check.html', data)
