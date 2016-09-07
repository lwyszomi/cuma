from django.utils.translation import ugettext_lazy as _
from requests.exceptions import HTTPError

from django.conf import settings

from accounts.models import DHIS2User
from dhis2.utils import get_client


class DHIS2AuthenticationException(Exception):
    pass


class DHIS2Authentication(object):

    FIELD_MAPPINGS = {
        'email': 'email',
        'firstName': 'first_name',
        'surname': 'last_name',
        'id': 'external_id'
    }

    def authenticate(self, username=None, password=None, **kwargs):
        if username in getattr(settings, 'SUPERUSER_LIST', ('admin',)):
            try:
                user = DHIS2User.objects.get(username=username)
                if user.check_password(password):
                    return user
                return None
            except DHIS2User.DoesNotExist:
                return None
        # Fetch user profile from selected endpoint
        profile = self.authenticate_user(username, password)
        if not profile:
            return None

        username = profile['userCredentials']['username']

        user_data = {
            model_field_name: profile.get(profile_field_name)
            for profile_field_name, model_field_name in self.FIELD_MAPPINGS.iteritems()
        }

        user, _ = DHIS2User.objects.update_or_create(
            username=username,
            defaults=user_data
        )
        return user

    @staticmethod
    def authenticate_user(username, password):
        if not username or not password:
            return None

        dhis_client = get_client()
        try:
            response = dhis_client.get_user_profile(username, password)
        except HTTPError:
            return None
        if not response:
            raise DHIS2AuthenticationException(_('Bad response from DHIS2 service.'))
        return response

    @staticmethod
    def get_user(user_id):
        try:
            return DHIS2User.objects.get(id=user_id)
        except DHIS2User.DoesNotExist:
            return None
