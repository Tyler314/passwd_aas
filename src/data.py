from dataclasses import dataclass

@dataclass
class Passwd:
    name: str
    password: str
    uid: int
    gid: int
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
    group_name: str
    passwd: str
    group_id: str
    group_list: list[str]
