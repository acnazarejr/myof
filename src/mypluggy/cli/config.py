"""CLI config subcommand entry."""

import click


@click.group()
@click.pass_context
def config(ctx: click.Context) -> None:
    """Hepls to manage the configuration of the MyPluggy CLI."""


@config.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize the configuration file."""
    click.echo("Criando uma nova configuração...")
    client_id = click.prompt("Digite o client_id", default=None, type=str)
    client_secret = click.prompt("Digite o client_secret", default=None, type=str)
