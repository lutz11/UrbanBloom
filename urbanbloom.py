import click

@click.group()
@click.version_option(version="0.1.0", prog_name="urbanbloom")
def cli():
    """
    A ranking model for metropolitan areas.
    """
    print("This is the main entry point")
    pass

@cli.command()
@click.option('--descend', 'sort_order', flag_value='descending', help='Sort in descending order.')
@click.option('--ascend', 'sort_order', flag_value='ascending', default=True, help='Sort in ascending order (default).')
def index(sort_order):
    """
    Displays a ranked index of metropolitan areas.
    """
    message = f"Indexing Sorting in {sort_order} order."
    click.echo(message)

if __name__ == "__main__":
    cli()
