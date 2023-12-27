import pytest

from ice_breaker.services.linkedin_service import LinkedInService
from ice_breaker.services.service import get_service_class, get_services_list


def test_get_service_class():
    assert get_service_class("linkedin") == LinkedInService


def test_get_service_class_with_invalid_service():
    with pytest.raises(ValueError):
        get_service_class("invalid_service")


def test_get_services_list():
    expected_services_list = ["linkedin"]
    assert get_services_list() == expected_services_list
