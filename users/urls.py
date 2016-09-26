from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from users.views import UserListView, ShowUserView, EditUserView, GetRoleView, SaveUserView, SaveLanguage, \
    UsersJsonView, CountriesJsonView, UserProfileJsonView, UserEditData

partial_patterns = [
    url(r'^users-list.html$', TemplateView.as_view(template_name='angular/partials/users-list.html'),
        name='users_list'),
    url(r'^user-profile.html$', TemplateView.as_view(template_name='angular/partials/user-profile.html'),
        name='user_profile'),
    url(r'^user-edit.html$', TemplateView.as_view(template_name='angular/partials/user-edit.html'),
        name='user_edit'),
]

json_patterns = [
    url(r'^users', UsersJsonView.as_view(), name='users'),
    url(r'^countries', CountriesJsonView.as_view(), name='countries'),
    url(r'^user_profile', UserProfileJsonView.as_view(), name='user_profile'),
    url(r'^user_edit', UserEditData.as_view(), name='user_edit')
]

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='users/app.html')),
    url(r'^show_user/(?P<user_id>[\w\.:-]+)/$', ShowUserView.as_view(), name="show_user"),
    url(r'^edit_user/(?P<user_id>[\w\.:-]+)/(?P<step>[1-3]{1})/$', EditUserView.as_view(), name="edit_user"),
    url(r'^get_role_by_name/$', GetRoleView.as_view(), name="get_role_by_name"),
    url(r'^save_user/$', SaveUserView.as_view(), name="save_user"),
    url(r'^(?P<user_id>[\w\.:-]+)/save_language/$', SaveLanguage.as_view(), name="save_language"),

    url(r'^partials/', include(partial_patterns, namespace='partials')),
    url(r'^json/', include(json_patterns, namespace='json'))
]
