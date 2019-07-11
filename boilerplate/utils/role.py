import enum
class Role(enum.Enum):
    """
    Role of a user in the system.
    """
    admin = 'admin'
    moderator = 'moderator'
    viewer = 'viewer'