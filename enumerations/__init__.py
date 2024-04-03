from enum import Enum


class Charts(str, Enum):
    MELON = 'Melon'
    GENIE = 'Genie'
    FLO = 'Flo'
    BUGS = 'Bugs'
    YOUTUBE = 'YouTube'
    SPOTIFY = 'Spotify'
    BILLBOARD = 'Billboard'

    @classmethod
    def _missing_(cls, value: str):
        value = value.casefold()

        for member in cls:
            if member.casefold() == value:
                return member

        return None

    @classmethod
    def contains(cls, value: str):
        if cls._missing_(value) is not None:
            return True
        return False

