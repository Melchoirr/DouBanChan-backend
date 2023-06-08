import os
import platform
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template import loader
from tools.imports import *
from DouBanChan_Backend.settings import EMAIL_HOST_USER


def send_email(email, u_id):
    url = '' + str(u_id)
    if platform.system() == "Linux":
        url = os.path.join("https://milimili.super2021.com:8000/sender/activate/", url)
    else:
        url = os.path.join("http://10.193.206.15:8000/sender/activate/", url)
    data = {'url': url}
    email_title = r"欢迎注册豆瓣酱图书影视交流平台"
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
        data = {"title": "感谢注册", "message": "注册豆瓣酱图书影视交流平台成功！", "url": "http://10.193.206.15:8000/"}
        return render(request, 'EmailContent-check.html', data)
    except Exception:
        data = {"title": "注册失败", "message": "注册豆瓣酱图书影视交流平台失败！", "url": "http://10.193.206.15:8000/"}
        return render(request, 'EmailContent-check.html', data)


def find(request):
    try:
        user = User.objects.get(u_name=request.POST['u_name'])
        data = {"title": "找回密码", "message": "找回密码成功！", "url": "http://10.193.206.15:8000/", "password": user.u_password}
        email_body = loader.render_to_string('EmailContent-find.html', data)
        msg = EmailMessage(r"z找回密码", email_body, EMAIL_HOST_USER, [user.u_email])
        msg.content_subtype = 'html'
        send_status = msg.send()
        return send_status
    except Exception:
        return ERR_OTHER
