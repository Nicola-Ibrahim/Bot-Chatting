import uuid
from dataclasses import dataclass, field

from src.building_blocks.domain.entity import AggregateRoot

from .entities.permission import Permission
from .entities.role import Role
from .value_objects.address import Address
from .value_objects.email import Email
from .value_objects.name import Name
from .value_objects.password import Password
from .value_objects.phone_number import PhoneNumber
from .value_objects.user_id import UserId
from .value_objects.username import Username


@dataclass
class User(AggregateRoot):
    """
    Represents a user in the domain with attributes and operations.
    """

    _id: UserId
    _name: Name
    _username: Username
    _email: Email
    _phone_number: PhoneNumber
    _address: Address
    _password: Password
    _permissions: list[Permission] = field(default_factory=list)
    _role: Role | None = None
    _bio: str | None = None
    _profile_picture_url: str | None = None
    _email_notifications: bool = True
    _sms_notifications: bool = False
    _is_verified: bool = False
    _is_active: bool = True

    def __post_init__(self):
        if not isinstance(self._permissions, list):
            raise ValueError("Permissions must be a list of Permission objects.")
        if self._role and not isinstance(self._role, Role):
            raise ValueError("Role must be an instance of the Role class.")
        if not self._username.value.islower():
            raise ValueError("Username must be lowercase.")

    # Property methods for read access to private fields
    @property
    def id(self) -> UserId:
        return self._id

    @property
    def name(self) -> Name:
        return self._name

    @property
    def username(self) -> Username:
        return self._username

    @property
    def email(self) -> Email:
        return self._email

    @property
    def phone_number(self) -> PhoneNumber:
        return self._phone_number

    @property
    def address(self) -> Address:
        return self._address

    @property
    def permissions(self) -> list[Permission]:
        return self._permissions

    @property
    def role(self) -> Role | None:
        return self._role

    @property
    def bio(self) -> str | None:
        return self._bio

    @property
    def profile_picture_url(self) -> str | None:
        return self._profile_picture_url

    @property
    def email_notifications(self) -> bool:
        return self._email_notifications

    @property
    def sms_notifications(self) -> bool:
        return self._sms_notifications

    @property
    def is_verified(self) -> bool:
        return self._is_verified

    @property
    def is_active(self) -> bool:
        return self._is_active

    # Factory method for creating a user
    @classmethod
    def create_user(
        cls,
        username: Username,
        email: Email,
        raw_password: str,
        name: Name,
        address: Address,
        phone_number: PhoneNumber,
        role: Role,
        permissions: list[Permission],
    ):
        hashed_password = Password.hash_password(raw_password=raw_password)
        user_id = UserId.create(value=uuid.uuid4())
        return cls(
            _id=user_id,
            _name=name,
            _username=username,
            _email=email,
            _password=hashed_password,
            _phone_number=phone_number,
            _address=address,
            _permissions=permissions,
            _role=role,
        )

    # Role Management
    def assign_role(self, role: Role):
        if self._role:
            raise ValueError("User already has a role assigned.")
        self._role = role
        for permission in role.permissions:
            self.add_permission(permission)

    def remove_role(self):
        if not self._role:
            raise ValueError("No role assigned to remove.")
        self._role = None
        self._permissions.clear()

    # Permission Management
    def add_permission(self, permission: Permission):
        if permission not in self._permissions:
            self._permissions.append(permission)
        else:
            raise ValueError(f"Permission '{permission.name}' is already assigned to the user.")

    def remove_permission(self, permission: Permission):
        if permission in self._permissions:
            self._permissions.remove(permission)
        else:
            raise ValueError(f"Permission '{permission.name}' is not assigned to the user.")

    # Login Operations
    def can_login(self) -> bool:
        if not self._is_verified:
            raise ValueError("User account is not verified.")
        if not self._is_active:
            raise ValueError("User account is not active.")
        return True

    def login(self):
        if self.can_login():
            # Simulate a successful login
            return True

    # Username Management
    def change_username(self, username: Username, username_uniqueness_checker: "UsernameUniquenessChecker"):
        username.check_against_rules()
        if not username_uniqueness_checker.is_unique(username):
            raise ValueError("Username is already taken.")
        self._username = username

    # Profile Management
    def update_profile(self, bio: str | None = None, profile_picture_url: str | None = None):
        if bio:
            self._bio = bio
        if profile_picture_url:
            self._profile_picture_url = profile_picture_url

    # Settings Management
    def update_settings(self, email_notifications: bool, sms_notifications: bool):
        self._email_notifications = email_notifications
        self._sms_notifications = sms_notifications

    # Permission Checking
    def has_permission(self, permission_name: str) -> bool:
        return any(permission.name == permission_name for permission in self._permissions)
