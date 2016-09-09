from django.http import JsonResponse
from django.views.generic.base import TemplateView, View
import math
import users.queries as queries
from collections import defaultdict
from django.conf import settings
import json

from accounts.mixins import LoginRequiredMixin
from users.utils import generate_user_view_format, generate_hierarchy


class UserListView(LoginRequiredMixin, TemplateView):

    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        users = queries.get_users()

        kwargs['users'] = json.dumps(generate_user_view_format(users))
        kwargs['countries'] = json.dumps(generate_hierarchy())

        return super(UserListView, self).get_context_data(**kwargs)


class ShowUserView(LoginRequiredMixin, TemplateView):

    template_name = 'users/show_user.html'

    def get_context_data(self, **kwargs):
        user = queries.get_user(kwargs['user_id'])
        organizations = user['organisationUnits']
        org_dict = defaultdict(list)
        for org in organizations:
            country = None
            if len(org['ancestors']) >= settings.COUNTRY_LEVEL:
                country = org['ancestors'][settings.COUNTRY_LEVEL-1]

            if country:
                org_dict[country['displayName']].append(org['displayName'])
            else:
                org_dict[org['displayName']] = []

        kwargs['dhis_user'] = user
        kwargs['organizations'] = dict(org_dict)
        return super(ShowUserView, self).get_context_data(**kwargs)


class EditUserView(LoginRequiredMixin, TemplateView):

    template_name = 'users/edit_user.html'

    def get_context_data(self, **kwargs):
        user = queries.get_user(kwargs['user_id'])
        organization_units = queries.get_organization_units()
        roles = queries.get_user_roles()
        for org in organization_units:
            org['sectors'] = []
            sectors = []
            if 'code' not in org:
                continue
            for role in roles:
                if org['code'] in role['displayName']:
                    sector = role['displayName'].split(": %s- " % org['code'])
                    if len(sector) == 2:
                        sectors.append(sector[1])
            org['sectors'] = list(set(sectors))
        user_groups = queries.get_user_groups()
        kwargs['dhis_user'] = json.dumps(user)
        kwargs['organisationUnits'] = json.dumps(organization_units)
        kwargs['countryLvl'] = settings.COUNTRY_LEVEL
        kwargs['userGroups'] = json.dumps(user_groups)
        return super(EditUserView, self).get_context_data(**kwargs)


class GetRoleView(View):

    def get(self, request, *agrs, **kwargs):
        role_name = request.GET.get('role_name', '')
        role = ''
        if role_name:
            role = queries.get_role_by_name(role_name)
        return JsonResponse(data={'role': role})
