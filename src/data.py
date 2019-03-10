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

@dataclass
class Group:
    group_name: str
    passwd: str
    group_id: str
    group_list: list[str]
