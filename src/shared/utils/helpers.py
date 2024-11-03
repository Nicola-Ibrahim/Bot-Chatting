import importlib
import pkgutil
from inspect import getmembers
from typing import Any, Generator, Iterable, Type, TypeVar, Union

# Define a generic type variable for the members
T = TypeVar("T")


def import_modules_from_package(package: str) -> Generator[Any, None, None]:
    """
    Imports all modules within the specified package.

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


def get_members_from_modules_or_packages(
    modules: Union[Any, Iterable[Any]], member_type: Type[T] | None = None, name: str | None = None
) -> Generator[T, None, None]:
    """
    Retrieves members from the given module(s) or package(s) based on type or name.

    Args:
        modules (Union[Any, Iterable[Any]]): A single module or an iterable of imported modules.
        member_type (Type[T], optional): The type of member to filter (e.g., APIRouter). Defaults to None.
        name (str, optional): The specific name of the member to retrieve. Defaults to None.

    Yields:
        Iterable[T]: An iterable of members that match the specified type or name.
    """
    # If a single module is provided, convert it to a list for uniformity
    if not isinstance(modules, Iterable):
        modules = [modules]

    # Use a generator for efficient membership retrieval
    for module in modules:
        for member_name, member in getmembers(module):
            if (member_type is not None and isinstance(member, member_type)) or (
                name is not None and member_name == name
            ):
                yield member


def import_members_from_package(
    package: str, member_type: Type[T] | None = None, name: str | None = None
) -> Generator[T, None, None]:
    """
    Imports and retrieves specified members from all modules in a package.

    Args:
        package (str): The package path (e.g., 'src.api.v1.endpoints').
        member_type (Type[T], optional): The type of member to filter. Defaults to None.
        name (str, optional): The specific name of the member to retrieve. Defaults to None.

    Yields:
        Iterable[T]: An iterable of members imported from the modules in the specified package.
    """
    modules = import_modules_from_package(package)
    return get_members_from_modules_or_packages(modules, member_type, name)
