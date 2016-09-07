from dhis2.client import DHIS2Client
from django.conf import settings


def get_client():
    return DHIS2Client(settings.DHIS2_API_URL, settings.DHIS2_USERNAME, settings.DHIS2_PASSWORD)