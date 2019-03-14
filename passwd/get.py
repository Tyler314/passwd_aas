from .data import Passwd, Group
import os


__all__ = ["Get"]


class Get:
    """
    Handle the business logic for extracting information from the passwd and group files.
    Framework independent, used with flask but can be used by any framework or library desirable.
    """

    def __init__(self):
        """Create a Get object.

        Fields:
            path_to_passwd : String
                Full path to the password file.

            path_to_group : String
                Full path to the group file.

            passwd_map : Dictionary
                Map of uids of users, to an object of the Passwd dataclass, for all the users of the passwd file.

            group_map : Dictionary
                Map of names of groups, to an object of the Group dataclass, for all the groups of the group file.

            groups_by_user_name : Dictionary
                Map of user names, to a list of all the groups with that associated user name.

            passwd_last_updated : Number
                Time of the most recent modification to the passwd file in memory.

            group_last_updated : number
                Time of the most recent modification to the group file in memory.

        """
        self.path_to_passwd = "/etc/passwd"
        self.path_to_group = "/etc/group"
        self.passwd_map = dict()
        self.passwd_last_updated = -1
        self.group_map = dict()
        self.group_last_updated = -1
        self.groups_by_user_name = dict()

    def set_passwd_path(self, path):
        """Set the full path to the passwd file, and resets the time last update field.

        Parameters:
            path : String
                Full path to the passwd file.

        Returns:
            None
        """
        self.path_to_passwd = path
        self.passwd_last_updated = -1
        self.group_last_updated = -1
        self.groups_by_user_name.clear()
        self.passwd_map.clear()


    def set_group_path(self, path):
        """Set the full path to the group file, and resets the time last update field.

        Parameters:
            path : String
                Full path to the group file.

        Returns:
            None
        """
        self.path_to_group = path
        self.passwd_last_updated = -1
        self.group_last_updated = -1
        self.groups_by_user_name.clear()
        self.group_map.clear()

    def users(self, name=None, uid=None, gid=None, comment=None, home=None, shell=None):
        """Return list of user dictionaries. Optional keyword arguments used to filter users of interest.
        If no arguments specified, returns all users from the specified passwd file.
        If no user is found based on search criteria, return an empty list.

        Parameters: (Query fields.)
            name : String (Optional)

            uid : Integer (Optional)

            gid : Integer (Optional)

            comment : String (Optional)

            home : String (Optional)

            shell : String (Optional)

        Returns:
            List[dict]
                Each dictionary of the list represents a single user.
        """
        query = Passwd(name, None, uid, gid, comment, home, shell)
        self._read_passwd_file()
        output = []
        for line in self.passwd_map.values():
            if query == line:
                output.append(vars(line))
        return output

    def groups(self, name=None, gid=None, members=None):
        """Return list of dictionaries. Optional keyword arguments used to filter groups of interest.
        If no arguments specified, returns all groups from the specified group file.
        If no group is found based on search criteria, return an empty list.

        Parameters: (Query fields.)
            name : String (Optional)

            gid : Integer (Optional)

            members : List[String] (Optional)

        Returns:
            List[dict]
                Each dictionary of the list represents a single group.
        """
        self._read_group_file()
        output = []
        for line in self.group_map.values():
            if (
                (name is None or name == line.name)
                and (gid is None or gid == line.gid)
                and (members is None or set(members).issubset(set(line.members)))
            ):
                output.append(vars(line))
        return output

    def groups_by_uid(self, uid):
        """Return list of dictionaries. Special case, look up group based on required argument uid.
        If no group exists with specified uid, return an empty list.

        Parameters: (Query fields.)
            uid : String

        Returns:
            List[dict]
                Each dictionary of the list represents a single group.
        """
        self._read_passwd_file()
        self._read_group_file()
        user_name = self.passwd_map[uid].name
        return [vars(group) for group in self.groups_by_user_name.get(user_name, [])]

    def _read_passwd_file(self):
        """Private method that updates the class field 'passwd_map' with data classes of all the users in the passwd file.
        Only updates if the file was modified since the last time the method was called. Keep track of last modified time.
        """
        if os.path.getmtime(self.path_to_passwd) != self.passwd_last_updated:
            self.passwd_last_updated = os.path.getmtime(self.path_to_passwd)
            with open(self.path_to_passwd, "r") as f:
                for line in f:
                    line = line.strip()
                    if line == "" or line.startswith("#"):
                        continue
                    values = line.split(":")
                    values[2] = int(values[2])
                    values[3] = int(values[3])
                    self.passwd_map[values[2]] = Passwd(*values)

    def _read_group_file(self):
        """Private method that updates the class field 'group_map' with data classes of all the groups in the group file.
        Only updates if the file was modified since the last time the method was called. Keep track of last modified time.
        """
        if os.path.getmtime(self.path_to_group) != self.group_last_updated:
            self.group_last_updated = os.path.getmtime(self.path_to_group)
            with open(self.path_to_group, "r") as f:
                for line in f:
                    line = line.strip()
                    if line == "" or line.startswith("#"):
                        continue
                    *values, users = line.split(":")
                    values[2] = int(values[2])
                    user_list = [s.strip() for s in users.split(",")]
                    if user_list == [""]:
                        user_list = []
                    group = Group(*values, user_list)
                    self.group_map[values[0]] = group
                    for user in user_list:
                        if user not in self.groups_by_user_name:
                            self.groups_by_user_name[user] = [group]
                        else:
                            self.groups_by_user_name[user].append(group)
