import json

import pytest

from ice_breaker.services.abstract_service import AbstractService


class TestableAbstractService(AbstractService):
    def _scrape_profile_production(self, force_local=False, force_scraping=False):
        return {}

    def _clean_profile(self, *args, **kwargs):
        return {}


# Fixtures
@pytest.fixture
def service_development():
    return TestableAbstractService("test_id", "development", "/test/path")


# Test Initialization
def test_initialization(service_development):
    service = service_development
    assert service.profile_id == "test_id"
    assert service.environment == "development"
    assert service.profiles_path == "/test/path"


# Test Scrape Profile
def test_scrape_profile_production(monkeypatch):
    def mock_scrape(*args, **kwargs):
        return {"data": "production data"}

    monkeypatch.setattr(TestableAbstractService, "_scrape_profile_production", mock_scrape)
    service = TestableAbstractService("test_id", "production", "/test/path")
    result = service.scrape_profile()
    assert result == {"data": "production data"}


def test_scrape_profile_development(monkeypatch, service_development):
    def mock_scrape(*args, **kwargs):
        return {"data": "development data"}

    monkeypatch.setattr(TestableAbstractService, "_load_profile", mock_scrape)
    service = service_development
    result = service.scrape_profile()
    assert result == {"data": "development data"}


# TODO: Fix this test
# Test Save Profile
# def test_save_profile_success(monkeypatch, service_development):
#     def mock_dump(*args, **kwargs):
#         return None
#     monkeypatch.setattr('json.dump', mock_dump)
#     service = service_development
#     # Set up the necessary profile data
#     service.profile_data = {"name": "Test Name"}
#
#     # Test the save_profile method
#     result = service.save_profile()
#     assert result == service.profile_data


def test_save_profile_no_data(service_development):
    service = service_development
    # Ensure profile_data is not set
    service.profile_data = None

    # Test that ValueError is raised
    with pytest.raises(ValueError):
        service.save_profile()


# TODO: Fix this test
# def test_save_profile_external():
#     service = service_development
#     profile_data = {"name": "Test Name"}
#
#     # Test the save_profile_external method
#     result = service.save_profile_external(profile_data)
#     assert result == profile_data


# Test Load Profile
def test_load_profile_success(monkeypatch, service_development):
    def mock_open(*args, **kwargs):
        class MockFile:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

            def read(self):
                return json.dumps({"name": "Test Name"})

        return MockFile()

    monkeypatch.setattr("builtins.open", mock_open)
    service = service_development
    result = service.load_profile()
    assert result == {"name": "Test Name"}
    assert service.profile_data == {"name": "Test Name"}


def test_load_profile_not_found(monkeypatch, service_development):
    monkeypatch.setattr("os.path.exists", lambda path: False)
    service = service_development
    with pytest.raises(FileNotFoundError):
        service.load_profile()


# Test Get Profile Slug and Path
def test_get_profile_slug_and_path():
    service = TestableAbstractService("Test ID", "development", "/test/path")
    service.service_name = "test_service"
    slug = service._get_profile_slug()
    assert slug == "test_id"  # Assuming slugify turns 'Test ID' to 'test_id'

    path = service._get_profile_path()
    assert (path == "/test/path/test_service__test_id.json") | (path == "/test/path\\test_service__test_id.json")


def test_download_profile(service_development):
    service = service_development

    # Mock the scrape_profile method
    def mock_scrape_profile(*args, **kwargs):
        return {"data": "development data"}

    service.scrape_profile = mock_scrape_profile

    # Mock the save_profile method
    def mock_save_profile(*args, **kwargs):
        return {"data": "development data"}

    service.save_profile = mock_save_profile

    # Mock the clean_profile method
    def mock_clean_profile(*args, **kwargs):
        return {"data": "development data"}

    service.clean_profile = mock_clean_profile

    service.download_profile()
    assert service.profile_data == {"data": "development data"}
