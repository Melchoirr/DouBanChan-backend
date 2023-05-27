import json

from django.http import HttpResponse

from models.models import Picture
from tools.imports import *


def upload(request):  # ERR?
    re = {}
    if request.method == 'POST':
        p_content = request.FILES['p_content']
        picture = Picture(p_content=p_content)
        picture.save()
        re['msg'] = 0
        re['picture'] = picture.to_dict()
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def get_picture_by_id(p_id):
    if Picture.objects.filter(p_id=p_id):
        return Picture.objects.get(p_id=p_id)
    return None
