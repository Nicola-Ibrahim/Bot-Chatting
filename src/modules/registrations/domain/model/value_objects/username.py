import dataclasses
import datetime
import re


@dataclasses.dataclass
class UsernameCanBeChangedAtMostOnceAMonth:
    changed_at: datetime.datetime

    def check(self):
        if (datetime.datetime.now() - self.changed_at()) > 30:
            raise UserNameCantBeChanged()


@dataclasses.dataclass(frozen=True)
class Username:
    value: str
    changed_at: datetime

    def __post_init__(self):
        if len(self.value) < 3 or len(self.value) > 20:
            raise ValueError("Username must be between 3 and 20 characters.")
        if not re.match("^[a-zA-Z0-9_.-]+$", self.value):
            raise ValueError("Username can only contain letters, numbers, dots, hyphens, and underscores.")

    def check_against_rules(self):
        rules = [UsernameCanBeChangedAtMostOnceAMonth(self.changed_at)]

        for rule in rules:
            rule.check()
