from django.conf import settings

from dhis2.client import DHIS2Client


def get_users():
     dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
     return dhis_client.get_users()


def get_user(user_id):
    dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    return dhis_client.get_user(user_id)


def get_organization_units():
    dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    return dhis_client.get_organization_units()


def get_countries():
    dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    return dhis_client.get_countries()


def get_user_groups():
    dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    return dhis_client.get_user_groups()


def get_user_roles():
    dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    return dhis_client.get_user_roles()


def get_role_by_name(role_name):
    dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    return dhis_client.get_role_by_name(role_name)


def save_user(user):
    dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    return dhis_client.save_user(user)


def get_dashboard_role():
    dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    return dhis_client.get_dashboard_role()


def get_users_without_role(role_id):
    dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    return dhis_client.get_users_without_role(role_id)
