import click
from click import option
import pandas as pd

from lib.dataset_ops import DatasetOps
from lib.file_ops import FileOps


@click.group()
@click.version_option(version="0.1.0", prog_name="urbanbloom")
def cli():
    """
    A ranking model for metropolitan areas.
    """
    print("This is the main entry point")
    pass

@cli.command()
@click.option('--descend', 'sort_order', flag_value='false', help='Sort in descending order.')
@click.option('--ascend', 'sort_order', flag_value='true', default=True, help='Sort in ascending order (default).')
@click.argument('column1')
@click.argument('column2')
@click.argument('column3')
def index(sort_order, column1, column2, column3):
    """
    Displays a ranked index of metropolitan areas.
    """
    message = f"Showing selected columns."
    click.echo(message)

    datasetoperator = DatasetOps()
    fileoperator = FileOps()

    UBdf = datasetoperator.generate_urban_bloom_index()
    output_UBdf = UBdf[["Geographic Area Name", "urbanbloom_rank"]]

    options = [column1, column2, column3]

    for option in options:
        output_UBdf = datasetoperator.add_column(UBdf, column_name=option)

    sorted_UBdf = datasetoperator.sort_df(output_UBdf, ascending=sort_order)

    output_path = fileoperator.get_output_dir()
    output_file = fileoperator.append_path(output_path, "output.csv")
    sorted_UBdf.to_excel(output_file, index=False, engine='openpyxl')



@cli.command()
@click.option('--descend', 'sort_order', flag_value='false', help='Sort in descending order.')
@click.option('--ascend', 'sort_order', flag_value='true', default=True, help='Sort in ascending order (default).')
@click.argument('column1')
@click.argument('column2')
@click.argument('column3')
def show(sort_order, column1, column2, column3):
    """
    Displays a ranked index of metropolitan areas.
    """
    message = f"Indexing Sorting in {sort_order} order."
    click.echo(message)

    datasetoperator = DatasetOps()
    fileoperator = FileOps()

    options = [column1, column2, column3]

    file = fileoperator.find_file_from_column(options[0])
    df = pd.read_csv(file)
    df = df[["Geographic Area Name", options[0]]]

    for option in options:
        df = datasetoperator.addColumn(df, column_name=option, ascending=sort_order)

    output_path = fileoperator.get_output_dir()
    output_file = fileoperator.append_path(output_path, "output.csv")
    df.to_excel(output_file, index=False, engine='openpyxl')


if __name__ == "__main__":
    cli()
