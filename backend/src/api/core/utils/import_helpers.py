import importlib
import os
import pkgutil
from functools import lru_cache
from importlib import import_module
from inspect import getmembers
from typing import Any, Generator, Type, TypeVar

from pydantic_settings import BaseSettings

# Define a generic type variable for the member
T = TypeVar("T")


def import_modules_from_package(package_name: str) -> Generator[Any, None, None]:
    """
    Import all modules within the specified package.

    Args:
        package_name (str): The dot-separated package path (e.g., 'src.api.v1.endpoints').

    Yields:
        Iterable[Any]: An iterable of imported modules.
    """
    # Load the package and get its __path__ for module discovery
    package = importlib.import_module(package_name)
    package_path = package.__path__

    # Iterate through all modules within the package and yield them
    for _, module_name, _ in pkgutil.iter_modules(package_path):
        yield importlib.import_module(f"{package_name}.{module_name}")


def extract_members_from_module(
    module: Any, member_type: Type[T] | None = None, member_name: str | None = None
) -> Generator[T, None, None]:
    """
    Retrieves members from a given module based on type or name.

    Args:
        module (Any): The imported module.
        member_type (Type[T], optional): The type of member to filter (e.g., APIRouter). Defaults to None.
        member_name (str, optional): The specific name of the member to retrieve. Defaults to None.

    Yields:
        Iterable[T]: An iterable of members that match the specified type or name.
    """
    for name, member in getmembers(module):
        if (member_type is not None and isinstance(member, member_type)) or (
            member_name is not None and name == member_name
        ):
            yield member


def extract_members_from_package(
    package_name: str, member_type: Type[T] | None = None, member_name: str | None = None
) -> Generator[T, None, None]:
    """
    Imports all modules from a package and retrieves specified members from them.

    Args:
        package_name (str): The package path (e.g., 'src.api.v1.endpoints').
        member_type (Type[T], optional): The type of member to filter. Defaults to None.
        member_name (str, optional): The specific name of the member to retrieve. Defaults to None.

    Yields:
        Iterable[T]: An iterable of members imported from the modules in the specified package.
    """
    # First, import all modules from the package
    modules = import_modules_from_package(package_name)

    # Then, extract the desired members from the modules
    for module in modules:
        yield from extract_members_from_module(module, member_type, member_name)


@lru_cache
def get_settings() -> BaseSettings:
    """
    Dynamically loads the appropriate settings module based on environment.
    Caches the result for performance.

    Environment Detection Priority:
    1. Explicit ENV environment variable
    2. APP_ENV environment variable
    3. Defaults to 'dev'

    Raises:
        ImportError: If the settings module cannot be imported
        AttributeError: If the settings module is invalid
    """
    env = os.getenv("ENV") or os.getenv("APP_ENV", "dev").lower()

    try:
        # Dynamic import based on environment
        settings_module = import_module(f"app.core.config.{env}_settings")

        # Validate the module has a Settings class
        if not hasattr(settings_module, "Settings"):
            raise AttributeError(f"{env}_settings.py must define a 'Settings' class")

        return settings_module.Settings()

    except ImportError as e:
        raise ImportError(
            f"Could not import settings for environment '{env}'. Ensure app/core/config/{env}_settings.py exists."
        ) from e
    except Exception as e:
        raise RuntimeError(f"Failed to load settings for environment '{env}': {str(e)}") from e
