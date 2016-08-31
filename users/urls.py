from django.conf.urls import url

from users.views import UserListView, ShowUserView

urlpatterns = [
    url(r'^$', UserListView.as_view()),
    url(r'^show_user/(?P<user_id>[\w\.:-]+)/$', ShowUserView.as_view(), name="show_user")
]
