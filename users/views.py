from django.views.generic.base import TemplateView

import users.queries as queries


class UserListView(TemplateView):

    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        kwargs['users'] = queries.get_users()
        return super(UserListView, self).get_context_data(**kwargs)
