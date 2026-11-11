"""End-to-end test: ciphwren-dav between a CalDAV client and an Etebase server.

Needs a server that allows signups (e.g. the ciphwren-server test-server image), given in
ETEBASE_TEST_API_URL. Run with: python -m unittest tests.test_caldav
"""

import os
import re
import subprocess
import sys
import tempfile
import time
import unittest
import uuid

import requests
from etebase import Account, Client, User

SERVER_URL = os.environ.get("ETEBASE_TEST_API_URL", "http://localhost:3735/")
DAV_PORT = "37359"
DAV_URL = f"http://127.0.0.1:{DAV_PORT}"
COL_TYPE = "etebase.vevent"
# Clients always send a body: an empty PROPFIND (which should mean all properties) fails with a 500
PROPFIND_BODY = (
    '<?xml version="1.0"?><d:propfind xmlns:d="DAV:"><d:prop><d:resourcetype/><d:getetag/></d:prop></d:propfind>'
)
PROPFIND_HEADERS = {"Depth": "1", "Content-Type": "application/xml"}
CALENDAR_QUERY_BODY = (
    '<?xml version="1.0"?><c:calendar-query xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">'
    '<d:prop><d:getetag/><c:calendar-data/></d:prop><c:filter><c:comp-filter name="VCALENDAR"/></c:filter>'
    "</c:calendar-query>"
)


def make_event(uid):
    return (
        "BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//ciphwren-dav tests//EN\r\n"
        f"BEGIN:VEVENT\r\nUID:{uid}\r\nDTSTAMP:20260101T120000Z\r\n"
        "DTSTART:20260102T120000Z\r\nDTEND:20260102T130000Z\r\n"
        f"SUMMARY:{uid}\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n"
    )


def wait_for(check, what, timeout=60):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if check():
            return
        time.sleep(1)
    raise AssertionError(f"Timed out waiting for {what}")


class TestCalDAV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.username = "dav" + uuid.uuid4().hex[:10]
        cls.password = "pw-" + uuid.uuid4().hex
        account = Account.signup(
            Client("ciphwren-dav-tests", SERVER_URL), User(cls.username, "test@example.com"), cls.password
        )
        col_mgr = account.get_collection_manager()
        col = col_mgr.create(COL_TYPE, {"name": "Calendar"}, b"")
        col_mgr.upload(col, None)
        cls.col_uid = col.uid
        account.logout()

        cls.data_dir = tempfile.TemporaryDirectory()
        cls.env = dict(
            os.environ,
            CIPHWREN_URL=SERVER_URL,
            CIPHWREN_DATA_DIR=cls.data_dir.name,
            CIPHWREN_LISTEN_PORT=DAV_PORT,
            CIPHWREN_SERVER_HOSTS=f"127.0.0.1:{DAV_PORT}",
        )
        script = os.path.join(os.path.dirname(__file__), "..", "scripts", "ciphwren-dav")
        out = subprocess.run(
            [sys.executable, script, "manage", "add", cls.username, "--password", cls.password],
            env=cls.env,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        cls.dav_auth = (cls.username, out.split("Password:")[1].split()[0])

        cls.dav = subprocess.Popen([sys.executable, script], env=cls.env)
        wait_for(lambda: cls._reachable(), "ciphwren-dav to start")

    @classmethod
    def tearDownClass(cls):
        cls.dav.terminate()
        cls.dav.wait(10)
        cls.data_dir.cleanup()

    @staticmethod
    def _reachable():
        try:
            requests.get(DAV_URL, timeout=2)
            return True
        except requests.ConnectionError:
            return False

    def _login(self):
        return Account.login(Client("ciphwren-dav-tests", SERVER_URL), self.username, self.password)

    def _server_events(self):
        account = self._login()
        try:
            col_mgr = account.get_collection_manager()
            col = col_mgr.fetch(self.col_uid, None)
            items = col_mgr.get_item_manager(col).list(None).data
            return [bytes(item.content).decode() for item in items if not item.deleted]
        finally:
            account.logout()

    def _discover(self):
        # Like a client looking for its calendars; this makes ciphwren-dav sync the collection list
        response = requests.request(
            "PROPFIND", f"{DAV_URL}/{self.username}/", auth=self.dav_auth, headers=PROPFIND_HEADERS, data=PROPFIND_BODY
        )
        self.assertEqual(response.status_code, 207, response.text)

    def _dav_events(self):
        """The events of the calendar, fetched with a REPORT like clients do (a GET of one event fails)."""
        self._discover()
        response = requests.request(
            "REPORT",
            f"{DAV_URL}/{self.username}/{self.col_uid}/",
            auth=self.dav_auth,
            headers=PROPFIND_HEADERS,
            data=CALENDAR_QUERY_BODY,
        )
        self.assertEqual(response.status_code, 207, response.text)
        return re.findall(r"BEGIN:VCALENDAR.*?END:VCALENDAR", response.text, re.S)

    def test_event_from_client_reaches_server(self):
        self._discover()
        uid = "from-client-" + uuid.uuid4().hex
        response = requests.put(
            f"{DAV_URL}/{self.username}/{self.col_uid}/{uid}.ics",
            data=make_event(uid),
            auth=self.dav_auth,
            headers={"Content-Type": "text/calendar"},
        )
        self.assertEqual(response.status_code, 201, response.text)
        wait_for(lambda: any(f"SUMMARY:{uid}" in event for event in self._server_events()), "the event on the server")

    def test_event_from_server_reaches_client(self):
        uid = "from-server-" + uuid.uuid4().hex
        account = self._login()
        col_mgr = account.get_collection_manager()
        col = col_mgr.fetch(self.col_uid, None)
        item_mgr = col_mgr.get_item_manager(col)
        item_mgr.batch(
            [item_mgr.create({"name": uid, "mtime": int(time.time() * 1000)}, make_event(uid).encode())], None, None
        )
        account.logout()

        # ciphwren-dav syncs at most every 30 seconds when asked
        wait_for(
            lambda: any(f"SUMMARY:{uid}" in event for event in self._dav_events()), "the event in the calendar", 90
        )


if __name__ == "__main__":
    unittest.main()
