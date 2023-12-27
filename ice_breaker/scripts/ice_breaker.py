import click

from ice_breaker.scripts.download_profile import download_profile


# Define the CLI group
@click.group()
def ice_breaker():
    pass


# Add the CLI commands to the group
ice_breaker.add_command(download_profile)
