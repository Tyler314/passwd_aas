from .data import Passwd, Group
import os

class Get:
    def __init__(self, path_to_group, path_to_passwd):
        self.path_to_group = path_to_group
        self.path_to_passwd = path_to_passwd
        self.passwd_map = dict()
        self.passwd_last_updated = -1
        self.group_map = dict()
        self.group_last_updated = -1

    def users(self, name=None, uid=None, gid=None, comment=None, home=None, shell=None):
        pass

    def groups(self):
        pass
    
    def _read_passwd_file(self):
        if os.path.getmtime(self.path_to_passwd) != self.passwd_last_updated:
            self.passwd_last_updated = os.path.getmtime(self.path_to_passwd)
            with open(self.path_to_passwd, "r") as f:
                for line in f:
                    values = line.split(":")
                    self.passwd_map[values[0]] = Passwd(*values)

    def _read_group_file(self):
        if os.path.getmtime(self.path_to_group) != self.group_last_updated:
            self.group_last_updated = os.path.getmtime(self.path_to_group)
            with open(self.path_to_group, "r") as f:
                for line in f:
                    *values, users = line.split(':')
                    self.group_map[values[0]] = Group(*values, list(users))
