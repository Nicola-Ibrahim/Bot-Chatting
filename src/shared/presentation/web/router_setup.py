from fastapi import APIRouter

from .utils.import_helpers import get_member_from_package

# Absolute paths of endpoint packages
PACKAGE_PATHS = [
    "src.accounts.presentation.api.v1.endpoints",
]

MEMBER_TYPE = APIRouter


def prepare_routers():
    """Prepares routers by importing them from specified packages."""
    routers = []
    for package_path in PACKAGE_PATHS:
        package_routers = get_member_from_package(package_path, member_type=MEMBER_TYPE)
        routers.extend(package_routers)
    return routers
