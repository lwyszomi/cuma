from django.conf.urls import url

from users.views import UserListView

urlpatterns = [
    url(r'^', UserListView.as_view()),
]
