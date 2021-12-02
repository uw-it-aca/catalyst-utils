from .base_settings import *
from google.oauth2 import service_account
import os

INSTALLED_APPS += [
    'catalyst_utils.apps.CatalystUtilsConfig',
    'supporttools',
    'userservice',
    'persistent_message',
    'rc_django',
    'webpack_loader',
]

MIDDLEWARE += [
    'userservice.user.UserServiceMiddleware',
]

TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'supporttools.context_processors.supportools_globals',
    'catalyst_utils.context_processors.google_analytics',
    'catalyst_utils.context_processors.django_debug',
]

if os.getenv('ENV', 'localdev') == 'localdev':
    DEBUG = True
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = os.getenv('IMPORT_DATA_ROOT', '/app/csv')
    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': os.path.join(BASE_DIR, 'catalyst_utils/static/webpack-stats.json'),
        }
    }
    MIGRATION_MODULES = {
        'catalyst_utils': 'catalyst_utils.test_migrations',
    }
else:
    RESTCLIENTS_DAO_CACHE_CLASS = 'catalyst_utils.cache.RestClientsCache'
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_PROJECT_ID = os.getenv('STORAGE_PROJECT_ID', '')
    GS_BUCKET_NAME = os.getenv('STORAGE_BUCKET_NAME', '')
    GS_LOCATION = os.path.join(os.getenv('STORAGE_DATA_ROOT', ''))
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        '/gcs/credentials.json')
    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': os.path.join(BASE_DIR, '/static/webpack-stats.json'),
        }
    }

USERSERVICE_VALIDATION_MODULE = 'catalyst_utils.dao.person.is_netid'
USERSERVICE_OVERRIDE_AUTH_MODULE = 'catalyst_utils.views.can_override_user'
RESTCLIENTS_ADMIN_AUTH_MODULE = 'catalyst_utils.views.can_proxy_restclient'
PERSISTENT_MESSAGE_AUTH_MODULE = 'catalyst_utils.views.can_manage_persistent_messages'

SUPPORTTOOLS_PARENT_APP = 'Catalyst'
SUPPORTTOOLS_PARENT_APP_URL = '/'

GRADEBOOK_RETENTION_YEARS = 5
CURRENT_USER_GROUP = 'u_acadev_catalyst_current-users'
