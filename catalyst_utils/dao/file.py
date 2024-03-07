# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
from io import BytesIO
import zipfile
import os


def read_file(path):
    if not default_storage.exists(path):
        raise ObjectDoesNotExist()

    with default_storage.open(path, mode='r') as f:
        content = f.read()

    return content


def write_file(path, data):
    with default_storage.open(path, mode='wb') as f:
        f.write(data)


def build_archive(paths):
    archive = BytesIO()
    zip_file = zipfile.ZipFile(archive, 'w')

    for path in paths:
        filename = os.path.basename(path)
        try:
            zip_file.writestr(filename, read_file(path), zipfile.ZIP_DEFLATED)
        except ObjectDoesNotExist:
            pass

    zip_file.close()

    if not len(zip_file.infolist()):
        raise ObjectDoesNotExist()

    archive.seek(0)
    return archive
