from enum import Enum


class ServiceType(Enum):
    """Enum for the different types of services."""

    LINKEDIN: str = "linkedin"
    TWITTER: str = "twitter"

    def __str__(self) -> str:
        """Returns the string representation of the service type."""
        return self.value

    def __repr__(self) -> str:
        """Returns the string representation of the service type."""
        return self.value
