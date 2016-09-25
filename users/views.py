from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls.base import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from django.contrib import messages

import users.queries as queries
from collections import defaultdict
from django.conf import settings
import json

from accounts.mixins import LoginRequiredMixin
from dhis2.utils import get_client
from users.models import RoleType
from users.utils import generate_user_view_format, generate_hierarchy


class BaseView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        kwargs['dhis_url'] = settings.DHIS2_URL
        return super(BaseView, self).get_context_data(**kwargs)


class UserListView(BaseView):

    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        users = queries.get_users()

        kwargs['users'] = json.dumps(generate_user_view_format(users))
        kwargs['countries'] = json.dumps(generate_hierarchy())

        return super(UserListView, self).get_context_data(**kwargs)


class ShowUserView(BaseView):

    template_name = 'users/show_user.html'

    def get_context_data(self, **kwargs):
        user = queries.get_user(kwargs['user_id'])
        organizations = user['organisationUnits']
        org_dict = defaultdict(list)
        user_roles = user['userCredentials']['userRoles']
        user_groups = user['userGroups']
        country_list = []
        for org in organizations:
            country = None
            if len(org['ancestors']) >= settings.COUNTRY_LEVEL:
                country = org['ancestors'][settings.COUNTRY_LEVEL-1]

            if country:
                country_list.append(country)
                org_dict[country['displayName']].append(org['displayName'])

            else:
                country_list.append(org)
                org_dict[org['displayName']] = []

        roles = {}
        groups = {}
        for country in country_list:
            r = []
            g = []
            if 'code' not in country:
                continue
            for role in user_roles:
                if country['code'] in role['displayName']:
                    r.append(role['displayName'])
            for group in user_groups:
                if country['code'] in group['displayName']:
                    g.append(group['displayName'])
            roles[country['displayName']] = r
            groups[country['displayName']] = g

        kwargs['dhis_user'] = user

        client = get_client()

        kwargs['user_language'] = client.get_user_ui_language(user['userCredentials']['username'])
        kwargs['organizations'] = dict(org_dict)
        kwargs['roles'] = dict(roles)
        kwargs['groups'] = dict(groups)
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
                    sector = role['displayName'].split("%s- " % org['code'])
                    if len(sector) == 2:
                        sectors.append(sector[1])
            org['sectors'] = list(set(sectors))
        user_groups = queries.get_user_groups()
        kwargs['roleTypes'] = json.dumps([{'name': x.name} for x in RoleType.objects.all().order_by('name')])
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


class SaveUserView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SaveUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *agrs, **kwargs):
        user = json.loads(request.body)
        response = queries.save_user(user)
        if response.status_code == 200:
            return JsonResponse(data={'redirect': reverse('show_user', kwargs={'user_id': user['id']})})
        else:
            return JsonResponse(data={'error': 'Error'})


class SaveLanguage(View):

    def post(self, request, *args, **kwargs):
        language_code = request.POST['language_code']
        client = get_client()
        user = queries.get_user(kwargs['user_id'])
        result = client.change_language(user['userCredentials']['username'], language_code)
        if not result:
            messages.error(self.request, 'Unexpected error occurred. Please try again.', extra_tags='danger')
        return redirect('show_user', user_id=kwargs['user_id'])
