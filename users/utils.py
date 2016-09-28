from django.http.response import JsonResponse
from django.urls import reverse

from django.conf import settings
from django.views.generic.base import View

from accounts.mixins import LoginRequiredMixin
from users import queries


class JsonView(View, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context_data = {}
        context_data.update(**kwargs)
        return context_data

    def get(self, request, *args, **kwargs):
        return JsonResponse(data=self.get_context_data())


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


def generate_hierarchy():
    countries = queries.get_countries()
    groups = queries.get_user_groups()
    roles = queries.get_user_roles()
    for country in countries:
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
    return countries
