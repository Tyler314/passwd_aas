from .data import Passwd, Group
import os


__all__ = ['Get']


class Get:
    def __init__(self, path_to_group, path_to_passwd):
        self.path_to_group = path_to_group
        self.path_to_passwd = path_to_passwd
        self.passwd_map = dict()
        self.passwd_last_updated = -1
        self.group_map = dict()
        self.group_last_updated = -1
        self.groups_by_user_name = dict()

    def users(self, name=None, uid=None, gid=None, comment=None, home=None, shell=None):
        query = Passwd(name, None, uid, gid, comment, home, shell)
        self._read_passwd_file()
        output = []
        for line in self.passwd_map.values():
            if query == line:
                output.append(vars(line))
        return output

    def groups(self, name=None, gid=None, members=None):
        self._read_group_file()
        output = []
        for line in self.group_map.values():
            if (name is None or name == line.name) and (gid is None or gid == line.gid) and \
                    (members is None or set(members).issubset(set(line.members))):
                output.append(vars(line))
        return output

    def groups_by_uid(self, uid):
        self._read_passwd_file()
        self._read_group_file()
        user_name = self.passwd_map[uid].name
        return [vars(group) for group in self.groups_by_user_name.get(user_name, [])]

    def _read_passwd_file(self):
        if os.path.getmtime(self.path_to_passwd) != self.passwd_last_updated:
            self.passwd_last_updated = os.path.getmtime(self.path_to_passwd)
            with open(self.path_to_passwd, "r") as f:
                for line in f:
                    values = line.split(":")
                    self.passwd_map[values[2]] = Passwd(*values)

    def _read_group_file(self):
        if os.path.getmtime(self.path_to_group) != self.group_last_updated:
            self.group_last_updated = os.path.getmtime(self.path_to_group)
            with open(self.path_to_group, "r") as f:
                for line in f:
                    *values, users = line.split(':')
                    user_list = list(users)
                    group = Group(*values, user_list)
                    self.group_map[values[0]] = group
                    for user in user_list:
                        self.groups_by_user_name.get(user, []).append(group)
