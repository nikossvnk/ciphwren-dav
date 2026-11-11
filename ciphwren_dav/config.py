# Copyright © 2017 Tom Hacohen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import shutil

from appdirs import user_config_dir, user_data_dir


def env(name, default=None):
    """The environment variable CIPHWREN_<name>, or ETESYNC_<name> as it was named before the rename"""
    return os.environ.get("CIPHWREN_" + name, os.environ.get("ETESYNC_" + name, default))


def _data_dir():
    given = env("DATA_DIR")
    if given:
        return given
    path = user_data_dir("ciphwren-dav", "ciphwren")
    # The data of a version from before the rename is moved to the new place, once
    old = user_data_dir("etesync-dav", "etesync")
    if os.path.isdir(old) and not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        shutil.move(old, path)
    return path


LISTEN_ADDRESS = env("LISTEN_ADDRESS", "localhost")
LISTEN_PORT = env("LISTEN_PORT", "37358")

DEFAULT_HOSTS = "{}:{}".format(LISTEN_ADDRESS, LISTEN_PORT)

SERVER_HOSTS = env("SERVER_HOSTS", DEFAULT_HOSTS)
# (where EteSync 1.0 accounts were configured, only read when migrating them)
LEGACY_CONFIG_DIR = env("CONFIG_DIR", user_config_dir("etesync-dav", "etesync"))
DATA_DIR = _data_dir()

DEFAULT_SERVER_URL = env("URL", "https://api.etebase.com/partner/etesync/")
LEGACY_ETESYNC_URL = env("URL", "https://api.etesync.com/")
DATABASE_FILE = env("DATABASE_FILE", os.path.join(DATA_DIR, "etesync_data.db"))
ETEBASE_DATABASE_FILE = os.environ.get("ETEBASE_DATABASE_FILE", os.path.join(DATA_DIR, "etebase_data.db"))

HTPASSWD_FILE = os.path.join(DATA_DIR, "htpaswd")
CREDS_FILE = os.path.join(DATA_DIR, "etesync_creds")

SSL_KEY_FILE = os.path.join(DATA_DIR, "etesync.key")
SSL_CERT_FILE = os.path.join(DATA_DIR, "etesync.crt")
