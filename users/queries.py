from django.conf import settings

from dhis2.client import DHIS2Client


def get_users():
    dhis_client = DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)
    return dhis_client.get_users()
