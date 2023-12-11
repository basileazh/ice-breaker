from enum import Enum

from pydantic import BaseModel, ValidationError, field_validator


class Environment(str, Enum):
    """
    Environment.
    """

    development = "development"
    production = "production"


class EnvironmentMode(BaseModel):
    """
    Environment mode.
    """

    mode: Environment

    @field_validator("mode")
    def check_mode(cls, v: str):
        if v not in [
            "development",
            "production",
        ]:
            raise ValidationError(f"Invalid mode value: {v}, must be either 'development' or 'production'")
        return v
