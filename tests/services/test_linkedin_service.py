import json

from ice_breaker.services.linkedin_service import LinkedInService

# TODO: Fix this test
# def test__scrape_profile_production(monkeypatch):
#     def mock_request(*args, **kwargs):
#         return {"data": "production data"}
#
#     monkeypatch.setattr("requests.get", mock_request)
#
#     def mock_get_settings(*args, **kwargs):
#         return "AAA"
#
#     monkeypatch.setattr("ice_breaker.core.settings.get_settings", mock_get_settings)
#
#     service = LinkedInService(
#         "https://www.linkedin.com/in/roberto-romano-4a5a8a1b/", "production"
#     )
#
#     result = service._scrape_profile_production()
#     assert result == {"data": "production data"}


def test__clean_profile():
    service = LinkedInService("https://www.linkedin.com/in/yann-lecun/", "development")
    with open("data/linkedin_sample_profile_unclean.json", encoding="utf-8") as fi:
        input_data = json.load(fi)
    with open("data/linkedin_sample_profile.json", encoding="utf-8") as fo:
        expected_output = json.load(fo)
    output = service._clean_profile(input_data)
    print("output", output)
    print("expected_output", expected_output)
    assert output == expected_output
