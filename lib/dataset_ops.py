import sys

import pandas as pd
import numpy as np
import os

from numpy.f2py.auxfuncs import throw_error
from sklearn.preprocessing import MinMaxScaler
from lib.file_ops import FileOps


class DatasetOps:
    def __init__(self):
        self.datasetPath = FileOps.get_dataset_dir()
        self.outputPath = FileOps.get_output_dir()
        self.project_dir = FileOps.get_project_dir()
        self.dataset = None
        self.dataset_columns = self.get_dataset_columns()

    def get_dataset_file(self, csv_file):
        self.dataset = pd.read_csv(os.path.join(self.datasetPath, csv_file))
        return self.dataset

    def get_dataset_columns(self):
        try:
            return self.dataset.columns.tolist()
        except Exception as e:
            return None

    def generate_urban_bloom_index(self):
        fileoperator = FileOps()
        urban_bloom_index_path = os.path.join("datasets", "Metro Area Dataset - MAP - Town to Urban Bloom Index.csv")
        if not fileoperator.file_exists_in_project(urban_bloom_index_path):

            income_file = "Metro Area Dataset - Income by Metro Area.csv"
            income_file_path = fileoperator.get_dataset_path(income_file)
            df = pd.read_csv(income_file_path)

            WEIGHTS = {"median_income": 0.4, "high_earner_percent": 0.4, "log_population": 0.2}

            column_rename_map = {
                "Geographic Area Name": "Geographic Area Name",
                "Population": "population",
                "Households - Median income (dollars)": "median_income",
                "Households - $150,000 to $199,999": "percent_150k_200k",
                "Households - $200,000 or more": "percent_200k_plus",
            }

            df = self.rename_columns_to_mapping(df, column_rename_map)

            df["high_earner_percent"] = df["percent_150k_200k"] + df["percent_200k_plus"]
            df["log_population"] = np.log1p(df["population"])

            # Convert columns to numeric, coercing errors to NaN (Not a Number)
            for col in [
                "population",
                "median_income",
                "percent_150k_200k",
                "percent_200k_plus",
            ]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            df = df.dropna(
                subset=["median_income", "population", "percent_150k_200k", "percent_200k_plus"]
            )

            # Select the features that will be part of our index
            features = df[["median_income", "high_earner_percent", "log_population"]]

            # Initialize the MinMaxScaler to scale features between 0 and 1
            scaler = MinMaxScaler()
            scaled_features = scaler.fit_transform(features)

            # Create a new DataFrame with the scaled features
            scaled_df = pd.DataFrame(
                scaled_features,
                columns=[
                    "norm_median_income",
                    "norm_high_earner_percent",
                    "norm_log_population",
                ],
                index=features.index,
            )

            # Join the scaled features back to the original DataFrame
            df = df.join(scaled_df)

            # Calculate the final UrbanBloom Potential Index using the defined weights
            df["urbanbloom_index"] = (
                    df["norm_median_income"] * WEIGHTS["median_income"]
                    + df["norm_high_earner_percent"] * WEIGHTS["high_earner_percent"]
                    + df["norm_log_population"] * WEIGHTS["log_population"]
            )


            # Sort the DataFrame by the new index in descending order
            df_ranked = df.sort_values(by="urbanbloom_index", ascending=False)

            df_sorted = df_ranked[["Geographic Area Name", "urbanbloom_index"]]
            df_rank_reset = df_sorted.reset_index(drop=True)

            df_rank_reset.to_csv(urban_bloom_index_path)
            return df_rank_reset
        else:
            file = fileoperator.get_dataset_path("Metro Area Dataset - MAP - Town to Urban Bloom Index.csv")
            df = pd.read_csv(file)
            return df

    @staticmethod
    def rename_columns_to_mapping(df, column_rename_map):
        """
        Function that takes in a column rename map and returns a new df
        with only the columns in that map
        """
        required_original_cols = list(column_rename_map.keys())
        df = df[required_original_cols].copy()
        df = df.rename(columns=column_rename_map)
        return df

    @staticmethod
    def add_column(df, column_name):
        # set file sheet to temp_df
        file = FileOps.find_file_from_column(column_name)
        temp_df = pd.read_csv(file)
        # ensure the needed columns exist
        if column_name not in temp_df.columns:
            print(f"[ERROR] '{column_name}' not in temp_df columns")
            return None

        # for each column if temp_df has column, add it to df
        reduced_temp_df = temp_df[["Geographic Area Name", column_name]]
        merged = None
        try:
            merged = df.merge(
                reduced_temp_df, how="left", on="Geographic Area Name"
            )
        except Exception:
            None

        return merged

    @staticmethod
    def sort_df(df, column_name, ascending=True):
        if ascending:
            return df.sort_values(by=[column_name], ascending=True)
        else:
            return df.sort_values(by=[column_name], ascending=False)