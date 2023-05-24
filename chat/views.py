from tools.imports import *


def create_chat(request):
    """
    /chat/create POST
    create new chat
    :param request: c_name c_description
    :return: json, msg = 0, c_id on success
    """
    re = {}
    if request.method == 'POST':
        c_name = request.POST['c_name']
        c_description = request.POST['c_description']
        default_profile_photo = get_picture_by_id(DEFAULT_PROFILE_PHOTO_ID)
        new_chat = Chat(c_name=c_name, c_description=c_description, c_profile_photo=default_profile_photo,
                        c_create_time=timezone.now(), c_last_modify_time=timezone.now(), c_father_group_id=None)
        new_chat.save()
        re['msg'] = 0
        re['chat'] = new_chat.to_dict()
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def delete_chat(request):
    """
    /chat/create POST
    delete media
    :param request: c_id
    :return: json, msg = 0 on success
    """
    re = {}
    if request.method == 'POST':
        chat_id = request.POST['c_id']
        if not Chat.objects.filter(c_id=chat_id):
            re['msg'] = ERR_CHAT_NOT_EXISTS
        else:
            chat = Chat.objects.get(c_id=chat_id)
            chat.delete()
            re['msg'] = 0
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))


def query_single_chat(request):
    """
    /chat/query_single POST
    query single chat
    :param request: c_id
    :return: json, msg = 0, chat on success
    """
    re = {}
    if request.method == 'POST':
        c_id = request.POST['c_id']
        if not Chat.objects.filter(c_id=c_id):
            re['msg'] = ERR_CHAT_NOT_EXISTS
        else:
            chat = Chat.objects.get(c_id=c_id)
            re['msg'] = 0
            re['chat'] = chat.to_dict()
    else:
        re['msg'] = ERR_REQUEST_METHOD_WRONG
    return HttpResponse(json.dumps(re))
