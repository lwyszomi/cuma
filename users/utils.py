from django.urls import reverse

from django.conf import settings
from users import queries


def generate_user_view_format(users):
    view_format = []
    for u in users:
        countries = {}
        sectors = {}
        for org in u['organisationUnits']:
            if len(org['ancestors']) >= settings.COUNTRY_LEVEL:
                key = org['ancestors'][2]['id']
                countries.update({key: org['ancestors'][2]})
                if len(org['ancestors']) > settings.COUNTRY_LEVEL:
                    key = org['ancestors'][3]['id']
                    sectors.update({key: org['ancestors'][3]})
                elif len(org['ancestors']) == settings.COUNTRY_LEVEL:
                    org_copy = dict(org)
                    key = org_copy['id']
                    del org_copy['ancestors']
                    sectors.update({key: org_copy})
            elif len(org['ancestors']) == settings.COUNTRY_LEVEL - 1:
                key = org['id']
                del org['ancestors']
                countries.update({key: org})

        view_format.append(dict(
            id=u['id'],
            displayName=u['displayName'],
            username=u['userCredentials']['username'],
            status='Inactive' if u['userCredentials']['disabled'] else "Active",
            show_url=reverse('show_user', kwargs={'user_id': u['id']}),
            edit_url=reverse('edit_user', kwargs={'user_id': u['id']}),
            countries=countries.values(),
            sectors=sectors.values(),
            userGroups=u['userGroups'],
            roles=u['userCredentials']['userRoles']
        ))
    return view_format


def generate_hierarchy():
    countries = queries.get_countries()
    groups = queries.get_user_groups()
    roles = queries.get_user_roles()
    for country in countries:
        country['groups'] = []
        country['roles'] = []
        if 'code' not in country:
            continue
        for group in groups:
            if country['code'] in group['displayName']:
                country['groups'].append(group)
        for role in roles:
            if country['code'] in role['displayName']:
                country['roles'].append(role)
    return countries
