import uuid
from abc import ABC, abstractmethod
from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, IntegrityError
from django.db.models import ManyToManyField

from ...core.application.user.exceptions import RepositoryError, UserObjNotFoundError, UserSaveError
from ...models import User


class UserRepository(AbstractUserRepository):
    def create_user(self, user_data: dict[str, Any]) -> User:
        try:
            many_to_many_data = {}
            for field_name in list(user_data.keys()):
                if isinstance(getattr(User, field_name, None), ManyToManyField):
                    many_to_many_data[field_name] = user_data.pop(field_name)

            user = User.objects.create_user(**user_data)

            for field_name, value in many_to_many_data.items():
                getattr(user, field_name).set(value)

            return user
        except IntegrityError as e:
            raise UserSaveError(f"Integrity error while creating user: {str(e)}")
        except DatabaseError as e:
            raise RepositoryError(f"Database error occurred while creating user: {str(e)}")
        except Exception as e:
            raise RepositoryError(f"Unexpected error occurred while creating user: {str(e)}")

    def update_user(self, user: User, update_data: dict[str, Any]) -> User:
        try:
            many_to_many_data = {}
            for field_name in list(update_data.keys()):
                if isinstance(getattr(User, field_name, None), ManyToManyField):
                    many_to_many_data[field_name] = update_data.pop(field_name)

            for field, value in update_data.items():
                setattr(user, field, value)
            user.save()

            for field_name, value in many_to_many_data.items():
                getattr(user, field_name).set(value)

            return user
        except IntegrityError as e:
            raise UserSaveError(f"Integrity error while updating user: {str(e)}")
        except DatabaseError as e:
            raise RepositoryError(f"Database error occurred while updating user: {str(e)}")
        except Exception as e:
            raise RepositoryError(f"Unexpected error occurred while updating user: {str(e)}")

    def get_user_by_id(self, user_id: int | str | uuid.UUID) -> User:
        if not isinstance(user_id, (int, str, uuid.UUID)):
            raise ValueError("User ID must be an integer, string, or UUID.")
        try:
            return User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            raise UserObjNotFoundError(f"User with ID {user_id} does not exist.")
        except DatabaseError as e:
            raise RepositoryError(f"Database error occurred while retrieving user by ID: {str(e)}")
        except Exception as e:
            raise RepositoryError(f"Unexpected error occurred while retrieving user by ID: {str(e)}")

    def get_user_by_email(self, email: str) -> User:
        if not isinstance(email, str):
            raise ValueError("Email must be a string.")
        try:
            return User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise UserObjNotFoundError(f"User with email {email} does not exist.")
        except DatabaseError as e:
            raise RepositoryError(f"Database error occurred while retrieving user by email: {str(e)}")
        except Exception as e:
            raise RepositoryError(f"Unexpected error occurred while retrieving user by email: {str(e)}")

    def remove_user(self, user_id: int) -> None:
        if not isinstance(user_id, int):
            raise ValueError("User ID must be an integer.")

        user = self.get_user_by_id(user_id)

        try:
            user.delete()
        except DatabaseError as e:
            raise RepositoryError(f"Database error occurred while deleting user: {str(e)}")
        except Exception as e:
            raise RepositoryError(f"Unexpected error occurred while deleting user: {str(e)}")

    def check_user_exists(self, email: str) -> bool:
        if not isinstance(email, str):
            raise ValueError("Email must be a string.")
        try:
            return User.objects.filter(email=email).exists()
        except DatabaseError as e:
            raise RepositoryError(f"Database error occurred while checking user existence: {str(e)}")
        except Exception as e:
            raise RepositoryError(f"Unexpected error occurred while checking user existence: {str(e)}")

    def is_user_active(self, user_id: int | str | uuid.UUID) -> bool:
        user = self.get_user_by_id(user_id)
        return user.is_active

    def is_user_verified(self, user_id: int | str | uuid.UUID) -> bool:
        user = self.get_user_by_id(user_id)
        return user.is_verified
