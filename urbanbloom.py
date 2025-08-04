import sys

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
@click.argument('columns', nargs=-1, required=True)
def index(sort_order, columns):
    """
    Displays a ranked index of metropolitan areas.
    """
    message = f"Showing selected columns."
    click.echo(message)

    datasetoperator = DatasetOps()
    fileoperator = FileOps()

    UBdf = datasetoperator.generate_urban_bloom_index()
    reduced_UBdf = UBdf[["Geographic Area Name", "urbanbloom_index"]]

    for column in columns:
        output_UBdf = datasetoperator.add_column(reduced_UBdf, column_name=column)
        reduced_UBdf = output_UBdf

    sorted_UBdf = datasetoperator.sort_df(output_UBdf, columns[0], ascending=sort_order)

    output_path = fileoperator.get_output_dir()
    output_file = fileoperator.append_path(output_path, "output.xlsx")
    sorted_UBdf.to_excel(output_file, index=False, engine='openpyxl')



@cli.command()
@click.option('--descend', 'sort_order', flag_value='false', help='Sort in descending order.')
@click.option('--ascend', 'sort_order', flag_value='true', default=True, help='Sort in ascending order (default).')
@click.argument('columns', nargs=-1, required=True)
def show(sort_order, columns):
    """
    Displays a ranked index of metropolitan areas.
    """
    message = f"Showing {columns} Sorted by {columns[0]}."
    click.echo(message)

    datasetoperator = DatasetOps()
    fileoperator = FileOps()


    file = fileoperator.find_file_from_column(columns[0])
    if file is None:
        print(f"No file found with column name {columns[0]}")
        sys.exit()
    df = pd.read_csv(file)
    init_df = df[["Geographic Area Name", columns[0]]]
    init = False
    for column in columns:
        if not init:
            init = True
            continue
        else:
            column_added_df = datasetoperator.add_column(init_df, column_name=column)
            init_df = column_added_df

    if column_added_df is None:
        print(f"No file found with the column name {column}")
        sys.exit()

    sorted_df = datasetoperator.sort_df(column_added_df, columns[0], ascending=sort_order)

    output_path = fileoperator.get_output_dir()
    output_file = fileoperator.append_path(output_path, "output.xlsx")
    sorted_df.to_excel(output_file, index=False, engine='openpyxl')


if __name__ == "__main__":
    cli()
