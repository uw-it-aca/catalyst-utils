from .base_settings import *
from google.oauth2 import service_account
import os

INSTALLED_APPS += [
    'catalyst_utils.apps.CatalystUtilsConfig',
    'supporttools',
    'userservice',
    'persistent_message',
    'rc_django',
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
    MEDIA_ROOT = os.getenv('MEDIA_ROOT', '/app/data')
    MIGRATION_MODULES = {
        'catalyst_utils': 'catalyst_utils.test_migrations',
    }
    CATALYST_SUPPORT_GROUP = 'u_test_group'
    CATALYST_ADMIN_GROUP = 'u_test_group'
else:
    RESTCLIENTS_DAO_CACHE_CLASS = 'catalyst_utils.cache.RestClientsCache'
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
            'OPTIONS': {
                'project_id': os.getenv('STORAGE_PROJECT_ID', ''),
                'bucket_name': os.getenv('STORAGE_BUCKET_NAME', ''),
                'location': os.path.join(os.getenv('STORAGE_DATA_ROOT', '')),
                'credentials': service_account.Credentials.from_service_account_file(
                    '/gcs/credentials.json'),
            }
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
    CATALYST_SUPPORT_GROUP = os.getenv('SUPPORT_GROUP',
                                       'u_acadev_catalyst_support-admins')
    CATALYST_ADMIN_GROUP = os.getenv('ADMIN_GROUP', 'u_acadev_catalyst_admins')
    CSRF_TRUSTED_ORIGINS = ['https://' + os.getenv('CLUSTER_CNAME')]

USERSERVICE_VALIDATION_MODULE = 'catalyst_utils.dao.person.is_netid'
USERSERVICE_OVERRIDE_AUTH_MODULE = 'catalyst_utils.views.can_override_user'
RESTCLIENTS_ADMIN_AUTH_MODULE = 'catalyst_utils.views.can_proxy_restclient'
PERSISTENT_MESSAGE_AUTH_MODULE = 'catalyst_utils.views.can_manage_persistent_messages'

SUPPORTTOOLS_PARENT_APP = 'Catalyst'
SUPPORTTOOLS_PARENT_APP_URL = '/'

GRADEBOOK_RETENTION_YEARS = 5
CURRENT_USER_GROUP = 'u_acadev_catalyst_current-users'

if os.getenv("ENV") == "localdev":
    VITE_MANIFEST_PATH = os.path.join(
        BASE_DIR, "catalyst_utils", "static", "manifest.json"
    )
else:
    VITE_MANIFEST_PATH = os.path.join(os.sep, "static", "manifest.json")
