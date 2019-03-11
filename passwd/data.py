from dataclasses import dataclass

@dataclass
class Passwd:
    name: str
    password: str
    uid: str
    gid: str
    comment: str
    home: str
    shell: str

    def __eq__(self, other):
        for key in self.__dict__:
            if self.__dict__.get(key) is None or other.__dict__.get(key) is None:
                continue
            if self.__dict__.get(key) != other.__dict__.get(key):
                return False
        return True

@dataclass
class Group:
    name: str
    passwd: str
    gid: str
    members: list
