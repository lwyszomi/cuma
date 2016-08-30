from django.conf.urls import url

from users.views import UserListView, ShowUserView, UserView

urlpatterns = [
    url(r'^$', UserListView.as_view()),
    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'^show_user/(?P<user_id>[\w\.:-]+)/$', ShowUserView.as_view(), name="show_user")
]
