from .base_settings import *
from google.oauth2 import service_account
import os

INSTALLED_APPS += [
    'catalyst_utils.apps.CatalystUtilsConfig',
    'userservice',
]

MIDDLEWARE += [
    'userservice.user.UserServiceMiddleware',
]

if os.getenv('ENV', 'localdev') == 'localdev':
    DEBUG = True
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = os.getenv('IMPORT_DATA_ROOT', '/app/csv')
else:
    RESTCLIENTS_DAO_CACHE_CLASS = 'catalyst_utils.cache.RestClientsCache'
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_PROJECT_ID = os.getenv('STORAGE_PROJECT_ID', '')
    GS_BUCKET_NAME = os.getenv('STORAGE_BUCKET_NAME', '')
    GS_LOCATION = os.path.join(os.getenv('STORAGE_DATA_ROOT', ''))
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        '/gcs/credentials.json')

#USERSERVICE_VALIDATION_MODULE = 'catalyst_utils.dao.person.is_netid'
#USERSERVICE_OVERRIDE_AUTH_MODULE = 'catalyst_utils.views.support.can_override_user'

CURRENT_USER_GROUPS = ['uw_staff', 'uw_affiliate', 'uw_student']
