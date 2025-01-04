from datetime import datetime, timezone

from sqlmodel import Field, SQLModel

from .manager import Manager


class Model(SQLModel):
    id: int | None = Field(default=None, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.updated_at = datetime.now(timezone.utc)

    @classmethod
    def set_manager(cls, engine):
        cls.manager = Manager(cls, engine)
