from dataclasses import dataclass


@dataclass
class Passwd:
    """
    Data class used to store user fields of the passwd file
    """

    name: str
    password: str
    uid: int
    gid: int
    comment: str
    home: str
    shell: str

    # Override equals function, used to compare two Passwd objects in the Get class.
    # Compare each field for equality, and disregard if either field is None.
    def __eq__(self, other):
        for key in self.__dict__:
            if self.__dict__.get(key) is None or other.__dict__.get(key) is None:
                continue
            if self.__dict__.get(key) != other.__dict__.get(key):
                return False
        return True


@dataclass
class Group:
    """
    Data class used to store group fields of the group file
    """

    name: str
    password: str
    gid: int
    members: list
