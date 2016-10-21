import re

from django.http import JsonResponse
from django.http.response import Http404, HttpResponse
from django.urls.base import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View, TemplateView

import users.queries as queries
from collections import defaultdict
from django.conf import settings
import json

from accounts.mixins import LoginRequiredMixin
from accounts.models import DHIS2User, CometServerConfiguration
from dhis2.utils import get_client
from users.models import RoleType
from users.utils import generate_user_view_format, generate_hierarchy, JsonView, user_has_permissions_to_org_unit


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        kwargs.update(
            user=DHIS2User.objects.get_by_natural_key(self.request.user.username),
            dhis2_url=CometServerConfiguration.objects.first().url
        )
        return super(HomeView, self).get_context_data(**kwargs)


class UsersJsonView(JsonView):

    def get_context_data(self, **kwargs):
        users = queries.get_users()

        allowed_users = []
        current_user = queries.get_user(self.request.user.external_id)
        for user in users:
            if not any([
                user_has_permissions_to_org_unit(current_user, org_unit)
                for org_unit in user['organisationUnits']
            ]):
                continue
            user['organisationUnits'] = filter(
                lambda x: user_has_permissions_to_org_unit(current_user, x),
                user['organisationUnits']
            )
            allowed_users.append(user)

        return super(UsersJsonView, self).get_context_data(users=generate_user_view_format(allowed_users))


class CountriesJsonView(JsonView):

    def get_context_data(self, **kwargs):
        return super(CountriesJsonView, self).get_context_data(
            countries=generate_hierarchy(self.request.user.external_id)
        )


class UserProfileJsonView(JsonView):

    def get_context_data(self, **kwargs):
        user_id = self.request.GET.get('user_id')
        if not user_id:
            raise Http404()
        user = queries.get_user(user_id)
        current_user = queries.get_user(self.request.user.external_id)
        organizations = user['organisationUnits']
        org_dict = defaultdict(list)
        user_roles = user['userCredentials']['userRoles']
        user_groups = user['userGroups']
        country_list = []
        for org in organizations:
            country = None
            if len(org['ancestors']) >= settings.COUNTRY_LEVEL:
                country = org['ancestors'][settings.COUNTRY_LEVEL - 1]

            if country:
                if not user_has_permissions_to_org_unit(current_user, country):
                    continue
                country_list.append(country)
                org_dict[country['displayName']].append(org['displayName'])
            else:
                if not user_has_permissions_to_org_unit(current_user, org):
                    continue
                country_list.append(org)
                org_dict[org['displayName']] = []

        roles = {}
        groups = {}
        other_roles = []
        regex = re.compile('.*:.*-.*')
        for country in country_list:
            r = []
            g = []
            if 'code' not in country:
                continue
            for role in user_roles:
                if country['code'] in role['displayName']:
                    r.append(role['displayName'])
                elif not regex.match(role['displayName']):
                    other_roles.append(role['displayName'])
            for group in user_groups:
                if country['code'] in group['displayName']:
                    g.append(group['displayName'])
            roles[country['displayName']] = r
            groups[country['displayName']] = g

        if other_roles:
            roles['Other Roles'] = sorted(list(set(other_roles)))

        kwargs['dhis_user'] = user

        client = get_client()

        user_language_code = client.get_user_ui_language(user['userCredentials']['username'])
        languages_dict = dict(settings.LANGUAGES)

        user_language = {
            'code': 'en',
            'name': 'English'
        }

        if user_language_code in languages_dict:
            user_language = {
                'code': user_language_code,
                'name': languages_dict[user_language_code]
            }

        kwargs['user_language'] = user_language
        kwargs['languages'] = [
            {'code': code, 'name': name}
            for code, name in settings.LANGUAGES
        ]
        kwargs['change_language_url'] = reverse('save_language', kwargs={'user_id': user['id']})
        kwargs['organisations'] = dict(org_dict)
        kwargs['roles'] = dict(roles)
        kwargs['groups'] = dict(groups)
        return super(UserProfileJsonView, self).get_context_data(**kwargs)


class UserEditData(JsonView):

    def get_context_data(self, **kwargs):
        user_edit = self.request.GET.get('user_id')
        if not user_edit:
            raise Http404()
        user = queries.get_user(user_edit)
        organization_units = queries.get_organization_units()
        roles = queries.get_user_roles()
        current_user = queries.get_user(self.request.user.external_id)

        user_organisation_units = []
        for org in organization_units:
            if not user_has_permissions_to_org_unit(current_user, org):
                continue
            org['sectors'] = []
            sectors = []
            if 'code' not in org:
                continue
            for role in roles:
                if org['code'] in role['displayName']:
                    sector = role['displayName'].split('-', 1)
                    if len(sector) == 2:
                        split_first_part = sector[0].split(':')
                        if len(split_first_part) == 2 and org['code'] in split_first_part[1]:
                            sectors.append(sector[1])
            org['sectors'] = list(set(sectors))
            user_organisation_units.append(org)
        user_groups = queries.get_user_groups()
        kwargs['roleTypes'] = [{'name': x.name} for x in RoleType.objects.all().order_by('name')]
        kwargs['dhis_user'] = user
        kwargs['organisationUnits'] = user_organisation_units
        kwargs['countryLvl'] = settings.COUNTRY_LEVEL
        kwargs['userGroups'] = user_groups
        return super(UserEditData, self).get_context_data(**kwargs)


class GetRoleView(View):

    def get(self, request, *agrs, **kwargs):
        role_name = request.GET.get('role_name', '')
        country_code = request.GET.get('country_code', '')
        sector = request.GET.get('sector', '')
        role = ''
        if role_name:
            role = queries.get_role_by_name(
                {
                    'role_name': role_name,
                    'country_code': country_code,
                    'sector': sector
                }
            )
        return JsonResponse(data={'role': role})


class ChangeUserStatusView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ChangeUserStatusView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *agrs, **kwargs):
        user = queries.get_user(kwargs['user_id'])
        user['userCredentials']['disabled'] = not user['userCredentials']['disabled']
        response = queries.save_user(user)

        if response.status_code == 200:
            return JsonResponse(data={})
        else:
            return JsonResponse(data={'error': 'Error'})


class SaveUserView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SaveUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *agrs, **kwargs):
        user = json.loads(request.body)
        response = queries.save_user(user)
        if response.status_code == 200:
            return JsonResponse({})
        else:
            return JsonResponse(data=response.json(), status=400)


class SaveLanguage(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SaveLanguage, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        language_code = body['language_code']
        client = get_client()
        user = queries.get_user(kwargs['user_id'])
        client.change_language(user['userCredentials']['username'], language_code)
        return HttpResponse(status=200)
