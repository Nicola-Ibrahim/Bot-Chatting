from dataclasses import dataclass

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class CreatorNameCannotBeEmptyRule(BaseBusinessRule):
    name: str
    code: str = ErrorCode.CREATOR_REMOVAL_ERROR
    message: str = "The name of the creator cannot be empty."
    error_type: str = ErrorType.BUSINESS_RULE_VIOLATION
