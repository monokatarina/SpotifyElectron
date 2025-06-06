"""Schema for User domain model"""

from dataclasses import dataclass
from enum import Enum

from app.spotify_electron.user.base_user_schema import (
    BaseUserAlreadyExistsError,
    BaseUserBadNameError,
    BaseUserDAO,
    BaseUserDocument,
    BaseUserDTO,
    BaseUserNotFoundError,
    BaseUserRepositoryError,
    BaseUserServiceError,
)


class UserDocument(BaseUserDocument):
    """Represents user data in the persistence layer"""

    playback_history: list[str]
    playlists: list[str]
    saved_playlists: list[str]


@dataclass
class UserDAO(BaseUserDAO):
    """Represents user data in the internal processing layer"""

    playback_history: list[str]
    playlists: list[str]
    saved_playlists: list[str]


@dataclass
class UserDTO(BaseUserDTO):
    """Represents user data in the endpoints transfer layer"""

    playback_history: list[str]
    playlists: list[str]
    saved_playlists: list[str]


class UserType(Enum):
    """Type/roles of users"""

    ARTIST = "artist"
    USER = "user"


def get_user_dao_from_document(document: UserDocument) -> UserDAO:
    """Get UserDAO from document by extracting all required fields.

    Args:
        document: The user document.

    Returns:
        A fully populated UserDAO object.
    """
    return UserDAO(
        name=document["name"],
        photo=document["photo"],
        register_date=document["register_date"],
        password=document["password"],
        playback_history=document.get("playback_history", []),
        playlists=document.get("playlists", []),
        saved_playlists=document.get("saved_playlists", []),
    )


def get_user_dto_from_dao(user_dao: UserDAO) -> UserDTO:
    """Convert UserDAO to UserDTO for data transfer.

    Args:
        user_dao: UserDAO object to convert.

    Returns:
        Converted UserDTO object.
    """
    return UserDTO(
        name=user_dao.name,
        photo=user_dao.photo,
        register_date=user_dao.register_date,
        playback_history=user_dao.playback_history,
        playlists=user_dao.playlists,
        saved_playlists=user_dao.saved_playlists,
    )


class UserRepositoryError(BaseUserRepositoryError):
    """Base user Repository Unexpected error"""

    ERROR = "Error accessing User REPOSITORY"

    def __init__(self):
        super().__init__(self.ERROR)


class UserNotFoundError(BaseUserNotFoundError):
    """User not found"""

    ERROR = "User not found"

    def __init__(self):
        super().__init__(self.ERROR)


class UserBadNameError(BaseUserBadNameError):
    """Bad name"""

    ERROR = "Bad parameters provided for user"

    def __init__(self):
        super().__init__(self.ERROR)


class UserAlreadyExistsError(BaseUserAlreadyExistsError):
    """Exception raised when a User already exists"""

    ERROR = "User already exists"

    def __init__(self):
        super().__init__(self.ERROR)


class UserServiceError(BaseUserServiceError):
    """Exception raised when there is an unexpected error in user service"""

    ERROR = "Error accessing User Service"

    def __init__(self):
        super().__init__(self.ERROR)
