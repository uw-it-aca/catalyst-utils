# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from memcached_clients import RestclientPymemcacheClient
import re

ONE_MINUTE = 60
ONE_HOUR = 60 * 60
ONE_DAY = 60 * 60 * 24


class RestClientsCache(RestclientPymemcacheClient):
    def get_cache_expiration_time(self, service, url, status=None):
        if 'pws' == service or 'gws' == service:
            if status == 200 or status == 401:
                return ONE_DAY
            elif status == 404:
                return ONE_DAY * 30
            else:
                return ONE_MINUTE
        elif 'catalyst' == service:
            return None
