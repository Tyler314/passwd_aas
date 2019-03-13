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

    def test_bad_get(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 404)

    def test_users(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)

    def test_single_user_queries(self):
        response = self.client.get("/users/query?name=root")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.passwd_to_dict("root:x:0:0:root:/root:/bin/bash"))
        response = self.client.get("/users/query?name=gopher")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.passwd_to_dict("gopher:x:13:30:gopher:/var/gopher:/sbin/nologin"))

    def test_multiple_user_queries(self):
        response = self.client.get("/users/query?name=root&shell=/bin/bash")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), self.passwd_to_dict("root:x:0:0:root:/root:/bin/bash"))

    def passwd_to_dict(self, *args):
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


