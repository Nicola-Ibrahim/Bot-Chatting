from dataclasses import dataclass


@dataclass
class UserProfile:
    bio: str = None
    profile_picture_url: str = None


@dataclass
class UserSettings:
    email_notifications: bool = True
    sms_notifications: bool = False
