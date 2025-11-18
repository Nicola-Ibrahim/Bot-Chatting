from dataclasses import dataclass, field

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ContentTextMustNotContainProfanityRule(BaseBusinessRule):
    """Business rule ensuring a message does not contain profane words.

    The rule is broken when any of the predefined profanities appear in the
    text. Imports remain correct as they reference ``src.building_blocks``.
    """

    text: str
    code: ErrorCode = field(default=ErrorCode.INVALID_INPUT, init=False)
    message: str = field(
        default="Content text must not contain profane language.",
        init=False,
    )
    error_type: ErrorType = field(default=ErrorType.VALIDATION_ERROR, init=False)

    def is_broken(self) -> bool:
        profanities = ["badword1", "badword2"]
        # The rule is broken if the text contains any profane word
        return any(profanity in self.text for profanity in profanities)
