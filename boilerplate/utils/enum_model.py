import enum
class Role(enum.Enum):
    """
    Role of a user in the system.
    """
    admin = 'admin'
    moderator = 'moderator'
    viewer = 'viewer'

class Action(enum.Enum):
    create = 'create'
    login = 'login'
    forgot = 'forgot'
    change = 'change'

class Gender(enum.Enum):
    male = 'male'
    female = 'female'