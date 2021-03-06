import passwd
import unittest
import os

HERE = os.path.abspath(os.path.dirname(__file__))


class TestPasswd(unittest.TestCase):
    def setUp(self):
        self.get = passwd.Get()
        self.get.set_passwd_path(HERE + os.sep + "passwd")
        self.get.set_group_path(HERE + os.sep + "group")

    def _group_to_list(self, *args):
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
        return output

    def test_group_count(self):
        self.assertEqual(len(self.get.groups()), 42)

    def test_get_all_groups(self):
        groups = dict()
        for group in self.get.groups():
            groups[group["name"]] = group
        with open(HERE + os.sep + "group", "r") as f:
            for line in f:
                name, password, gid, members = line.strip().split(":")
                members = [s.strip() for s in members.split(",")]
                if members == [""]:
                    members = []
                self.assertEqual(name, groups[name]["name"])
                self.assertEqual(password, groups[name]["password"])
                self.assertEqual(int(gid), groups[name]["gid"])
                self.assertEqual(members, groups[name]["members"])

    def test_single_query(self):
        self.assertEqual(self.get.groups(name="root"), self._group_to_list("root:x:0:"))
        self.assertEqual(self.get.groups(name="adm"), self._group_to_list("adm:x:4:username"))
        self.assertEqual(
            self.get.groups(name="cdrom"), self._group_to_list("cdrom:x:24:username, username1")
        )
        self.assertEqual(self.get.groups(gid=41), self._group_to_list("gnats:x:41:"))
        self.assertEqual(
            self.get.groups(gid=24), self._group_to_list("cdrom:x:24:username, username1")
        )
        self.assertEqual(self.get.groups(gid=29), self._group_to_list("audio:x:29:pulse"))
        self.assertEqual(self.get.groups(gid=102), self._group_to_list("crontab:x:102:"))
        self.assertEqual(
            self.get.groups(members=["username"]),
            self._group_to_list(
                "adm:x:4:username",
                "dialout:x:20:username",
                "cdrom:x:24:username, username1",
                "www-data:x:33:username",
                "plugdev:x:46:username",
            ),
        )
        self.assertEqual(
            self.get.groups(members=["pulse"]), self._group_to_list("audio:x:29:pulse")
        )

    def test_bad_query(self):
        self.assertEqual(self.get.groups(name="foo"), [])
        self.assertEqual(self.get.groups(name="bad name"), [])
        self.assertEqual(self.get.groups(gid=-1), [])
        self.assertEqual(self.get.groups(gid=-55), [])
        self.assertEqual(self.get.groups(name="daemon", gid=2, members=["not", "a", "member"]), [])
        self.assertEqual(self.get.groups(name="root", gid=1), [])

    def test_empty_members(self):
        self.assertEqual(self.get.groups(members=[]), self.get.groups())

    def test_multiple_queries(self):
        self.assertEqual(self.get.groups(name="root", gid=0), self._group_to_list("root:x:0:"))
        self.assertEqual(
            self.get.groups(name="adm", gid=4), self._group_to_list("adm:x:4:username")
        )
        self.assertEqual(
            self.get.groups(name="cdrom", gid=24, members=["username"]),
            self._group_to_list("cdrom:x:24:username, username1"),
        )
        self.assertEqual(
            self.get.groups(name="cdrom", gid=24, members=["username", "username1"]),
            self._group_to_list("cdrom:x:24:username, username1"),
        )
        self.assertEqual(
            self.get.groups(name="plugdev", members=["username"]),
            self._group_to_list("plugdev:x:46:username"),
        )

    def test_group_by_uid(self):
        self.assertEqual(
            self.get.groups_by_uid(uid=123),
            self._group_to_list(
                "adm:x:4:username",
                "dialout:x:20:username",
                "cdrom:x:24:username, username1",
                "www-data:x:33:username",
                "plugdev:x:46:username",
            ),
        )
        self.assertEqual(
            self.get.groups_by_uid(uid=789), self._group_to_list("cdrom:x:24:username, username1")
        )

    def test_update_group_file(self):
        self.get.set_group_path(HERE + os.sep + "group2")
        self.get.groups()
        with open(HERE + os.sep + "group2") as f:
            for line in f:
                name, password, gid, members = line.strip().split(":")
                members = [s.strip() for s in members.split(",")]
                if members == [""]:
                    members = []
                gid = int(gid)
                self.assertEqual(self.get.group_map[name].name, name)
                self.assertEqual(self.get.group_map[name].gid, gid)
                self.assertEqual(self.get.group_map[name].members, members)


if __name__ == "__main__":
    unittest.main()
