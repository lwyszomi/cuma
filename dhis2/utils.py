from django.conf import settings

from dhis2.client import DHIS2Client


def join_path_to_url(url, path):
    if not url.endswith('/'):
        url += '/'

    path = path.lstrip('/')
    return url + path


def get_client():
    from accounts.models import CometServerConfiguration
    comet_configuration_server = CometServerConfiguration.objects.first()
    return DHIS2Client(
        join_path_to_url(comet_configuration_server.url, 'api/{}/'.format(settings.DHIS2_API_VERSION)),
        comet_configuration_server.username,
        comet_configuration_server.password
    )
