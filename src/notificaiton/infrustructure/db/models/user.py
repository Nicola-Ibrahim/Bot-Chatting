from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def check_password(self, password):
        # Implement password hashing check here
        pass
