"""CLI main command group entry."""

import click

from .config import config


@click.group()
@click.option(
    "-c",
    "--config",
    "config_file",
    help="Path to the configuration file.",
    type=click.Path(writable=True),
    default="~/mypluggy.toml",
    show_default=True,
)
@click.pass_context
def mypluggy(ctx: click.Context, config_file: str):
    """MyPluggy CLI to interact with MeuPluggy.ai service."""
    ctx.ensure_object(dict)
    ctx.obj["config_file"] = config_file


mypluggy.add_command(config)


def main():
    """Main entry point."""
    mypluggy(max_content_width=120)


# if __name__ == "__main__":
#     main()
