from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseModel, PostgresDsn, field_validator


# The `Settings` class defines a set of configuration settings including project name, CORS origins, database connection
# details, and configuration options.
class Settings(BaseModel):
    PROJECT_NAME: str = "Auth Service"

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", check_fields=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        """
        The function `assemble_cors_origins` takes a string or a list of strings as input and returns a list of stripped
        strings if the input is a comma-separated string, otherwise it returns the input as is.

        Args:
            cls: The `cls` parameter in the `assemble_cors_origins` function represents the class to which the method
            belongs. In this case, it seems that the method is a class method, and `cls` would refer to the class itself.
            v (Union[str, List[str]]): The parameter `v` in the provided function `assemble_cors_origins` can be either a
            string or a list of strings.

        Returns:
            The function `assemble_cors_origins` returns a list of strings if the input `v` is a single string without square
            brackets, it returns the input as is if it is already a list or a string with square brackets, and raises a
            ValueError for any other input type.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # POSTGRES_SERVER: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    # DATABASE_URI: PostgresDsn | None = None

    # @field_validator("DATABASE_URI", check_fields=True)
    # def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
    #     """
    #     Check the databaase uri, if it is string then return it as correct
    #     if is not then constructs the database URI with taken values from
    #     Setting models

    #     Args:
    #         v (Optional[str]): The current value of the field being validated (DATABASE_URI in this case).
    #         values (Dict[str, Any]): A dictionary containing the current values of all fields in the model.

    #     Returns:
    #         Any: _description_

    #     """
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
