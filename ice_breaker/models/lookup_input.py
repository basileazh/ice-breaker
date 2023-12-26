from pydantic import BaseModel, Field


class LookupInput(BaseModel):
    """
    LinkedIn lookup agent input.
    """

    name: str = Field(
        title="Name",
        description="The name to lookup.",
    )
