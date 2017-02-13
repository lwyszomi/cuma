import json

from dhis2.utils import get_client
from users.utils import get_default_ldap_client


def get_users():
    dhis_client = get_client()
    return dhis_client.get_users()


def get_user(user_id):
    dhis_client = get_client()
    return dhis_client.get_user(user_id)


def get_user_by_username(username):
    dhis_client = get_client()
    return dhis_client.get_user_by_username(username)


def get_organization_units():
    dhis_client = get_client()
    return dhis_client.get_organization_units()


def get_countries():
    dhis_client = get_client()
    return dhis_client.get_countries()


def get_user_groups():
    dhis_client = get_client()
    return dhis_client.get_user_groups()


def get_user_roles():
    dhis_client = get_client()
    return dhis_client.get_user_roles()


def get_role_by_name(params):
    dhis_client = get_client()
    return dhis_client.get_role_by_name(params)


def save_user(user):
    dhis_client = get_client()
    return dhis_client.save_user(user)


def create_user(user):
    dhis_client = get_client()
    # Workaround: https://lists.launchpad.net/dhis2-devs/msg48137.html
    user_id = dhis_client.get_system_id()
    user['id'] = user_id
    user['userCredentials']['userInfo'] = {
        'id': user_id
    }
    return dhis_client.create_user(user)


def get_system_id():
    dhis_client = get_client()
    return dhis_client.get_system_id()


def get_dashboard_role():
    dhis_client = get_client()
    return dhis_client.get_dashboard_role()


def get_users_without_role(role_id):
    dhis_client = get_client()
    return dhis_client.get_users_without_role(role_id)


def get_organisation_unit_by_name(name):
    dhis_client = get_client()
    return dhis_client.get_organisation_unit_by_name(name)


def get_ldap_users(search='', countries=None, all_countries=False):
    if all_countries:
        countries_filter = '(co=*)'
    elif not countries:
        return []
    else:
        countries_filter = u''.join([u'(co={})'.format(country) for country in countries])
    ldap_client = get_default_ldap_client()
    if not search:
        query = u'(&(objectClass=user)(|{}))'.format(countries_filter)
    else:
        query = u'(&(|(mail={0}*)(sn={0}*)(givenName={0}*)(name={0}*))(|{1}))'.format(search, countries_filter)
    query = query.encode('utf-8')
    return ldap_client.run_query(query, ['mail', 'cn', 'sn', 'givenName', 'name', 'title', 'co'])


def get_ldap_user(email):
    ldap_client = get_default_ldap_client()
    try:
        return ldap_client.run_query(
            '(&(objectClass=user)(mail={}))'.format(email),
            ['mail', 'cn', 'sn', 'givenName', 'co']
        )[0]
    except IndexError:
        return None
