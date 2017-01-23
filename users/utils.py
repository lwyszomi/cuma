from django.http.response import JsonResponse
from django.urls import reverse

from django.conf import settings
from django.views.generic.base import View

from accounts.mixins import LoginRequiredMixin


class JsonView(View, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context_data = {}
        context_data.update(**kwargs)
        return context_data

    def get(self, request, *args, **kwargs):
        return JsonResponse(data=self.get_context_data())


def user_has_permissions_to_org_unit(dhis2_user, org_unit):
    organisation_units_id = [
        organisationUnit['id']
        for organisationUnit in dhis2_user['organisationUnits']
    ]
    return any([org_id in org_unit['path'] for org_id in organisation_units_id])


def generate_user_view_format(users):
    view_format = []
    for u in users:
        countries = {}
        for org in u['organisationUnits']:
            if len(org['ancestors']) >= settings.COUNTRY_LEVEL:
                key = org['ancestors'][2]['id']
                countries.update({key: org['ancestors'][2]})
            elif len(org['ancestors']) == settings.COUNTRY_LEVEL - 1:
                key = org['id']
                del org['ancestors']
                countries.update({key: org})

        view_format.append(dict(
            id=u['id'],
            displayName=u['displayName'],
            username=u['userCredentials']['username'],
            status='Inactive' if u['userCredentials']['disabled'] else "Active",
            change_status_url=reverse('change_status', kwargs={'user_id': u['id']}),
            countries=countries.values(),
            userGroups=u['userGroups'],
            roles=u['userCredentials']['userRoles']
        ))
    return view_format


def generate_hierarchy(user_id):
    from users import queries

    user = queries.get_user(user_id)

    countries = queries.get_countries()
    groups = queries.get_user_groups()
    roles = queries.get_user_roles()

    user_countries = []
    for country in countries:
        if not user_has_permissions_to_org_unit(user, country):
            continue

        country['roles'] = []
        country['groups'] = []
        if 'code' not in country:
            continue
        for role in roles:
            if country['code'] in role['displayName']:
                country['roles'].append(role)
        for group in groups:
            if country['code'] in group['displayName']:
                country['groups'].append(group)
        user_countries.append(country)
    return user_countries


def get_default_ldap_client():
    from ldap_integration.client import LDAPClient
    return LDAPClient(settings.LDAP_SERVER, settings.BASE_DN, settings.LDAP_USER, settings.LDAP_PASSWORD)
