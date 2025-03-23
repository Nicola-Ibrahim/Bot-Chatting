from src.building_blocks.domain.exception import BusinessRuleValidationException

from ....domain.users.interfaces.repository import AbstractUserRepository
from ....domain.users.root import User
from ....domain.users.value_objects.address import Address
from ....domain.users.value_objects.email import Email
from ....domain.users.value_objects.name import Name
from ....domain.users.value_objects.password import Password
from ....domain.users.value_objects.phone_number import PhoneNumber
from ....domain.users.value_objects.user_id import UserId
from ....domain.users.value_objects.username import Username
from ...configuration.command_handler import BaseCommandHandler
from .create_user_command import CreateUserCommand


class CreateUserCommandHandler(BaseCommandHandler):
    def __init__(self, user_repository: AbstractUserRepository):
        self._user_repository = user_repository

    def handle(self, command: CreateUserCommand) -> User:
        # Check if the username or email is already taken
        if self._user_repository.is_username_taken(command.username):
            raise BusinessRuleValidationException("Username is already taken.")
        if self._user_repository.is_email_taken(command.email):
            raise BusinessRuleValidationException("Email is already registered.")

        # Create user value objects
        user_id = UserId.create(value=command.user_id)
        name = Name.create(command.name)
        username = Username.create(command.username)
        email = Email.create(command.email)
        password = Password.hash_password(command.raw_password)
        phone_number = PhoneNumber.create(command.phone_number)
        address = Address.create(command.address)

        # Create the user entity
        user = User.create_user(
            user_id=user_id,
            username=username,
            email=email,
            password=password,
            name=name,
            address=address,
            phone_number=phone_number,
        )

        # Persist the user to the repository
        self._user_repository.save(user)

        return user
