import passwd
import unittest


class TestPasswd(unittest.TestCase):

    def setUp(self):
        self.get = passwd.Get("passwd", "group")

    def _strings_to_list_of_dicts(self, *args):
        output = []
        for arg in args:
            name, password, uid, gid, comment, home, shell = arg.strip().split(":")
            d = dict()
            d["name"] = name
            d["password"] = password
            d["uid"] = uid
            d["gid"] = gid
            d["comment"] = comment
            d["home"] = home
            d["shell"] = shell
            output.append(d)
        return output

    def test_user_count(self):
        self.assertEqual(len(self.get.users()), 36)

    def test_get_all_users(self):
        users = dict()
        for user in self.get.users():
            users[user["name"]] = user
        with open("passwd", "r") as f:
            for line in f:
                name, password, uid, gid, comment, home, shell = line.strip().split(":")
                self.assertEqual(name, users[name]["name"])
                self.assertEqual(password, users[name]["password"])
                self.assertEqual(uid, users[name]["uid"])
                self.assertEqual(gid, users[name]["gid"])
                self.assertEqual(comment, users[name]["comment"])
                self.assertEqual(home, users[name]["home"])
                self.assertEqual(shell, users[name]["shell"])

    def test_single_query(self):
        self.assertEqual(self.get.users(name="daemon"), self._strings_to_list_of_dicts("daemon:x:2:2:daemon:/sbin:/sbin/nologin"))
        self.assertEqual(self.get.users(uid="3"), self._strings_to_list_of_dicts("adm:x:3:4:adm:/var/adm:/sbin/nologin"))
        compare = []
        with open("passwd", "r") as f:
            for line in f:
                name, password, uid, gid, comment, home, shell = line.strip().split(":")
                if shell == "/sbin/nologin":
                    compare.append(line.strip())
        self.assertEqual(self.get.users(shell="/sbin/nologin"), self._strings_to_list_of_dicts(*compare))
