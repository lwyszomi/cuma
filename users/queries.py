from django.conf import settings

from dhis2.client import DHIS2Client


def get_users(fields, page_size, page):
    dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    return dhis_client.get_users(fields, page_size, page)


def get_user(user_id):
    dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    return dhis_client.get_user(user_id)
