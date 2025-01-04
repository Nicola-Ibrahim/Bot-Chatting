from enum import Enum


class RatingType(Enum):
    LIKE = "like"
    DISLIKE = "dislike"


class ConversationPermission(Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
