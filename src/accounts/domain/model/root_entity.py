import dataclasses
from typing import Optional

from src.shared.domain.entity import RootEntity

from .other_entity import UserProfile, UserSettings
from .value_objects import Address, Name, Password, Phone
from .value_objects.email import Email
from .value_objects.username import Username


@dataclasses.dataclass
class User(RootEntity):
    name: Name
    username: Username
    email: Email
    phone: Phone
    address: Address
    password: Password
    is_verified: bool
    is_active: bool
    permissions: list[Permission] = dataclasses.field(default_factory=list)
    role: Optional[Role] = None
    profile: UserProfile = dataclasses.field(default_factory=UserProfile)
    settings: UserSettings = dataclasses.field(default_factory=UserSettings)

    def __post_init__(self):
        if not isinstance(self.permissions, list):
            raise ValueError("Permissions must be a list of Permission objects.")
        if self.role and not isinstance(self.role, Role):
            raise ValueError("Role must be an instance of the Role class.")
        if not self.username.value.islower():
            raise ValueError("Username must be lowercase.")

    def can_login(self) -> bool:
        if not self.is_verified:
            return UserAccountNotVerifiedException()

        elif not self.is_verified:
            return UserAccountNotActiveException()

        return True

    def login(self):
        self.can_login()

        return True

    def change_username(self, username: str, username_uniqueness_checker: UsernameUniquenessChecker):

        # Check the username againt the rule
        self.username.check_against_rules()

        # Edit the username
        self.username = username

    def assign_role(self, role: Role):
        if self.role:
            raise ValueError("User already has a role assigned.")
        self.role = role
        # Add role permissions to user permissions
        for permission in role.permissions:
            self.add_permission(permission)

    def remove_role(self):
        if not self.role:
            raise ValueError("No role assigned to remove.")
        self.role = None
        self.permissions.clear()  # Clear permissions tied to the role

    # Permission Management
    def add_permission(self, permission: Permission):
        if permission not in self.permissions:
            self.permissions.append(permission)
        else:
            raise ValueError(f"Permission '{permission.name}' is already assigned to the user.")

    def remove_permission(self, permission: Permission):
        if permission in self.permissions:
            self.permissions.remove(permission)
        else:
            raise ValueError(f"Permission '{permission.name}' is not assigned to the user.")

    # Profile Management
    def update_profile(self, bio: Optional[str] = None, profile_picture_url: Optional[str] = None):
        if bio:
            self.profile.bio = bio
        if profile_picture_url:
            self.profile.profile_picture_url = profile_picture_url

    # Settings Management
    def update_settings(self, email_notifications: bool = True, sms_notifications: bool = False):
        self.settings.email_notifications = email_notifications
        self.settings.sms_notifications = sms_notifications

    # Check Permissions (e.g., for access control)
    def has_permission(self, permission_name: str) -> bool:
        return any(permission.name == permission_name for permission in self.permissions)
