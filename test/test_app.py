from passwd import app
from unittest import TestCase
import json
import os

HERE = os.path.abspath(os.path.dirname(__file__))


class TestIntegrations(TestCase):
    def setUp(self):
        self.client = app.app.test_client()
        app.GET.set_passwd_path(HERE + os.sep + "passwd")
        app.GET.set_group_path(HERE + os.sep + "group")

    def test_bad_user(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/users/query?name=bad")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/users/query?uid=-1")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/users/-1/groups")
        self.assertEqual(response.status_code, 404)

    def test_bad_group(self):
        response = self.client.get("/groups/query?name=bad")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/groups/query?uid=-1")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/groups/-1/groups")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/groups/query?member=bad_member")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/groups/-1")
        self.assertEqual(response.status_code, 404)

    def test_users(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)

    def test_single_user_queries(self):
        response = self.client.get("/users/query?name=root")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.users_to_json("root:x:0:0:root:/root:/bin/bash"))
        response = self.client.get("/users/query?name=gopher")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.users_to_json("gopher:x:13:30:gopher:/var/gopher:/sbin/nologin"))
        response = self.client.get("/users/query?uid=14")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.users_to_json("ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin"))
        response = self.client.get("/users/query?uid=99")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.users_to_json("nobody:x:99:99:Nobody:/:/sbin/nologin"))

    def test_multiple_user_queries(self):
        response = self.client.get("/users/query?name=root&shell=/bin/bash")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.users_to_json("root:x:0:0:root:/root:/bin/bash"))
        response = self.client.get("/users/query?name=oprofile&shell=/sbin/nologin&uid=16&gid=16")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.users_to_json("oprofile:x:16:16:Special user account to be used by OProfile:/home/oprofile:/sbin/nologin"))
        response = self.client.get("/users/query?comment=&home=/var/gdm")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.users_to_json("gdm:x:42:42::/var/gdm:/sbin/nologin"))
        response = self.client.get("/users/query?name=bin&uid=1&gid=1&home=/bin&comment=bin&shell=/sbin/nologin")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.users_to_json("bin:x:1:1:bin:/bin:/sbin/nologin"))

    def test_groups_by_user(self):
        response = self.client.get("/users/123/groups")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.groups_to_json("adm:x:4:username", "dialout:x:20:username", "cdrom:x:24:username, username1", "www-data:x:33:username", "plugdev:x:46:username", ))
        response = self.client.get("/users/789/groups")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.groups_to_json("cdrom:x:24:username, username1", ))

    def test_groups(self):
        response = self.client.get("/groups")
        self.assertEqual(response.status_code, 200)

    def test_single_groups_queries(self):
        response = self.client.get("/groups/query?name=cdrom")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.groups_to_json("cdrom:x:24:username, username1", ))
        response = self.client.get("/groups/query?member=username")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.groups_to_json("adm:x:4:username", "dialout:x:20:username", "cdrom:x:24:username, username1", "www-data:x:33:username", "plugdev:x:46:username", ))
        response = self.client.get("/groups/query?gid=29")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.groups_to_json("audio:x:29:pulse", ))

    def test_multiple_groups_queries(self):
        response = self.client.get("/groups/query?name=cdrom&gid=24&member=username&member=username1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.groups_to_json("cdrom:x:24:username, username1", ))
        response = self.client.get("/groups/query?name=plugdev&gid=46")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.groups_to_json("plugdev:x:46:username", ))
        response = self.client.get("/groups/query?name=syslog&gid=103")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.groups_to_json("syslog:x:103:", ))

    def test_groups_by_gid(self):
        pass


    def users_to_json(self, *args):
        output = []
        for arg in args:
            name, password, uid, gid, comment, home, shell = arg.strip().split(":")
            d = dict()
            d["name"] = name
            d["password"] = password
            d["uid"] = int(uid)
            d["gid"] = int(gid)
            d["comment"] = comment
            d["home"] = home
            d["shell"] = shell
            output.append(d)
        return json.dumps(output)

    def groups_to_json(self, *args):
        output = []
        for arg in args:
            name, password, gid, members = arg.strip().split(":")
            d = dict()
            d["name"] = name
            d["password"] = password
            d["gid"] = int(gid)
            users = [s.strip() for s in members.split(",")]
            if users == [""]:
                users = []
            d["members"] = users
            output.append(d)
        return json.dumps(output)


