from django.urls import path
from group.views import *

urlpatterns = [
    path("create/", create_group),
    path("delete/", delete_group),
    path("update_group_tag/", update_group_tag),
    path("update_group_profile/", update_group_profile),
    path("update_group_description/", update_group_description),
    path("update_group_nickname/", update_group_nickname),
    # path("query_single/", query_single_group),
    path("group_brief/", group_brief),
    # path("add_chat/", add_chat), 同create chat
    # path("delete_chat/", delete_chat),
    path("join_group/", join_group),
    path("quit_group/", quit_group),
    path("set_essence/", set_essence),
    path("set_top/", set_top),
    path("apply_admin/", apply_admin),
    path("cancel_admin/", cancel_admin),
    path("query_apply/", query_apply),
    path("grant_apply/", grant_apply),
    path("deny_apply/", deny_apply),
    path("query_group_by_tag/", query_group_by_tag)
]
