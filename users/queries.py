from dhis2.utils import get_client


def get_users():
    dhis_client = get_client()
    return dhis_client.get_users()


def get_user(user_id):
    dhis_client = get_client()
    return dhis_client.get_user(user_id)


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


def get_dashboard_role():
    dhis_client = get_client()
    return dhis_client.get_dashboard_role()


def get_users_without_role(role_id):
    dhis_client = get_client()
    return dhis_client.get_users_without_role(role_id)
