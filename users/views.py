from django.views.generic.base import TemplateView
import math
import users.queries as queries
from collections import defaultdict
import json


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


class EditUserView(TemplateView):

    template_name = 'users/edit_user.html'

    def get_context_data(self, **kwargs):
        user = queries.get_user(kwargs['user_id'])
        organization_units = queries.get_organization_units()
        kwargs['user'] = user

        def get_chunks(orgs):
            org_len = len(orgs)
            elem_in_chunks = int(math.ceil(org_len/3.0))
            for i in range(0, org_len, elem_in_chunks):
                yield [json.dumps(orgs[i:i+elem_in_chunks])]

        kwargs['organizationUnits'] = get_chunks(organization_units)

        return super(EditUserView, self).get_context_data(**kwargs)

