from enum import Enum


class Role(Enum):
    GERENTE = 'Gerente'
    EDITOR = 'Editor'
    DEFAULT = 'Default'


class ProjectType(Enum):
    ONLINE = 'ONLINE'
    GAVETA = 'GAVETA'
