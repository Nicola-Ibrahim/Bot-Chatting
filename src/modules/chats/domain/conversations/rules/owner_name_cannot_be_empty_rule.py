from dataclasses import dataclass

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class OwnerNameCannotBeEmptyRule(BaseBusinessRule):
    name: str
    code: str = ErrorCode.OWNER_REMOVAL_ERROR
    message: str = "The name of the owner cannot be empty."
    error_type: str = ErrorType.BUSINESS_RULE_VIOLATION
