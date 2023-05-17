from django.http import HttpResponse
from django.conf import settings
import os
import base64

from models.models import Picture


def getPicture(picture):


    # 读取图片文件内容
    with open(picture.p_content.path, 'rb') as f:
        image_data = f.read()

    # 返回图片作为响应
    return base64.b64encode(image_data).decode('utf-8') # type?


