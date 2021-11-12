from django.conf import settings
from uw_gws import GWS
from restclients_core.exceptions import DataFailureException


def is_current_uwnetid(uwnetid):
    gws = GWS()
    for group_id in getattr(settings, 'CURRENT_USER_GROUPS', []):
        try:
            if gws.is_member(group_id, uwnetid.lower()):
                return True
        except DataFailureException as err:
            if err.status == 404:
                pass
            else:
                raise
        return False


def get_uwnetid_admins(uwnetid):
    admins = []
    group_id = 'u_netid_{}_admins'.format(uwnetid.lower())
    try:
        for member in GWS().get_members(group_id):
            if member.is_uwnetid():
                admins.append(member.name)
    except DataFailureException as err:
        if err.status == 404:
            return admins
        else:
            raise
