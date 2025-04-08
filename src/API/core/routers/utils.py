from fastapi import APIRouter

from ..utils.import_helpers import extract_members_from_package

PACKAGE_PATHS = [
    "src.api.modules.chats.conversations",
]


def prepare_routers(router_type=APIRouter):
    """
    Prepare and return a list of APIRouter instances.

    This function iterates over the PACKAGE_PATHS, imports the routers from each package,
    and combines them into a single list.

    Returns:
        list: A list of APIRouter instances.
    """
    routers = []
    for package_path in PACKAGE_PATHS:
        package_routers = extract_members_from_package(package_path, member_type=router_type)
        routers.extend(package_routers)
    return routers
