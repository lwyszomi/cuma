from django.conf.urls import url

from users.views import UserListView, ShowUserView, EditUserView, GetRoleView

urlpatterns = [
    url(r'^$', UserListView.as_view(), name='users'),
    url(r'^show_user/(?P<user_id>[\w\.:-]+)/$', ShowUserView.as_view(), name="show_user"),
    url(r'^edit_user/(?P<user_id>[\w\.:-]+)/$', EditUserView.as_view(), name="edit_user"),
    url(r'^get_role_by_name/$', GetRoleView.as_view(), name="get_role_by_name")
]
