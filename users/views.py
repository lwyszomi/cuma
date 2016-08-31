from django.views.generic.base import TemplateView, View

import users.queries as queries
from collections import defaultdict


class UserListView(TemplateView):

    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        kwargs['users'] = queries.get_users()
        return super(UserListView, self).get_context_data(**kwargs)


class ShowUserView(TemplateView):

    template_name = 'users/show_user.html'

    def get_context_data(self, **kwargs):
        user = queries.get_user(kwargs['user_id'])
        organizations = user['organisationUnits']
        org_dict = defaultdict(list)
        for org in organizations:
            country = None
            if org['ancestors']:
                country = org['ancestors'][0]

            if country:
                org_dict[country['displayName']].append(org['displayName'])
            else:
                org_dict[org['displayName']] = []

        kwargs['user'] = user
        kwargs['organizations'] = dict(org_dict)
        return super(ShowUserView, self).get_context_data(**kwargs)
