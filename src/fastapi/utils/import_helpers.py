import importlib
import pkgutil
from inspect import getmembers
from typing import Any, Generator, Type, TypeVar

# Define a generic type variable for the member
T = TypeVar("T")


def get_modules_from_package(package: str) -> Generator[Any, None, None]:
    """
    Get all modules within the specified package.

    Args:
        package (str): The dot-separated package path (e.g., 'src.api.v1.endpoints').

    Yields:
        Iterable[Any]: An iterable of imported modules.
    """
    # Load the package and get its __path__ for module discovery
    package_module = importlib.import_module(package)
    package_path = package_module.__path__

    # Iterate through all modules within the package and yield them
    for _, module_name, _ in pkgutil.iter_modules(package_path):
        yield importlib.import_module(f"{package}.{module_name}")


def get_member_from_module(
    module: Any, member_type: Type[T] | None = None, name: str | None = None
) -> Generator[T, None, None]:
    """
    Retrieves members from a given module based on type or name.

    Args:
        module (Any): The imported module.
        member_type (Type[T], optional): The type of member to filter (e.g., APIRouter). Defaults to None.
        name (str, optional): The specific name of the member to retrieve. Defaults to None.

    Yields:
        Iterable[T]: An iterable of members that match the specified type or name.
    """
    for member_name, member in getmembers(module):
        if (member_type is not None and isinstance(member, member_type)) or (name is not None and member_name == name):
            yield member


def get_member_from_package(
    package: str, member_type: Type[T] | None = None, name: str | None = None
) -> Generator[T, None, None]:
    """
    Imports all modules from a package and retrieves specified members from them.

    Args:
        package (str): The package path (e.g., 'src.api.v1.endpoints').
        member_type (Type[T], optional): The type of member to filter. Defaults to None.
        name (str, optional): The specific name of the member to retrieve. Defaults to None.

    Yields:
        Iterable[T]: An iterable of members imported from the modules in the specified package.
    """
    # First, import all modules from the package
    modules = get_modules_from_package(package)

    # Then, extract the desired members from the modules
    for module in modules:
        yield from get_member_from_module(module, member_type, name)
