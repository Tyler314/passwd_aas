import passwd
import unittest


class TestPasswd(unittest.TestCase):

    def setUp(self):
        self.get = passwd.Get("passwd", "group")

    def _to_list(self, *args):
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
        self.assertEqual(self.get.users(name="daemon"), self._to_list("daemon:x:2:2:daemon:/sbin:/sbin/nologin"))
        self.assertEqual(self.get.users(uid="3"), self._to_list("adm:x:3:4:adm:/var/adm:/sbin/nologin"))
        self.assertEqual(self.get.users(uid="38"), self._to_list("ntp:x:38:38::/etc/ntp:/sbin/nologin"))
        self.assertEqual(self.get.users(uid="14"), self._to_list("ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin"))
        self.assertEqual(self.get.users(gid="50"), self._to_list("ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin"))
        self.assertEqual(self.get.users(comment="virtual console memory owner"), self._to_list("vcsa:x:69:69:virtual console memory owner:/dev:/sbin/nologin"))
        self.assertEqual(self.get.users(home="/var/spool/mqueue"), self._to_list("mailnull:x:47:47::/var/spool/mqueue:/sbin/nologin", "smmsp:x:51:51::/var/spool/mqueue:/sbin/nologin"))
        compare = []
        with open("passwd", "r") as f:
            for line in f:
                name, password, uid, gid, comment, home, shell = line.strip().split(":")
                if shell == "/sbin/nologin":
                    compare.append(line.strip())
        self.assertEqual(self.get.users(shell="/sbin/nologin"), self._to_list(*compare))

    def test_bad_query(self):
        self.assertEqual(self.get.users(name="foo"), [])
        self.assertEqual(self.get.users(uid="-1"), [])
        self.assertEqual(self.get.users(gid="bar"), [])
        self.assertEqual(self.get.users(comment="bad comment"), [])
        self.assertEqual(self.get.users(home="/not/real"), [])
        self.assertEqual(self.get.users(shell="false"), [])
        self.assertEqual(self.get.users(name="daemon", uid="2", gid="2", shell="/etc/news"), [])

    def test_multiple_queries(self):
        self.assertEqual(self.get.users(name="daemon", uid="2"), self._to_list("daemon:x:2:2:daemon:/sbin:/sbin/nologin"))
        self.assertEqual(self.get.users(name="daemon", uid="2", gid="2"),
                         self._to_list("daemon:x:2:2:daemon:/sbin:/sbin/nologin"))
        self.assertEqual(self.get.users(name="daemon", uid="2", comment="daemon"),
                         self._to_list("daemon:x:2:2:daemon:/sbin:/sbin/nologin"))
        self.assertEqual(self.get.users(name="daemon", uid="2", comment="daemon", home="/sbin", shell="/sbin/nologin"),
                         self._to_list("daemon:x:2:2:daemon:/sbin:/sbin/nologin"))
        self.assertEqual(self.get.users(name="mailnull", home="/var/spool/mqueue"),
                         self._to_list("mailnull:x:47:47::/var/spool/mqueue:/sbin/nologin"))
        self.assertEqual(self.get.users(uid="86", gid="86", shell="/sbin/nologin"), self._to_list("sabayon:x:86:86:Sabayon user:/home/sabayon:/sbin/nologin"))
