from click.testing import CliRunner

from ice_breaker.scripts.ice_breaker import ice_breaker


def test_download_profile():
    runner = CliRunner()
    result = runner.invoke(
        ice_breaker,
        ["download-profile", "linkedin", "https://www.linkedin.com/in/yann-lecun/"],
    )
    print(result.output)
    assert result.exit_code == 0
