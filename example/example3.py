import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.file_ops import FileOps
from lib.dataset_ops import DatasetOps

if __name__ == "__main__":

    datasetoperator = DatasetOps()
    df = datasetoperator.generate_urban_bloom_index()

    if df is None:
        print("Urban Bloom Index CSV already loaded.")
        df = datasetoperator.get_dataset_file("Metro Area Dataset - MAP - Town to Urban Bloom Index.csv")

    else:
        print("Urban Bloom Index CSV loaded.")

    print("Top 20 Metro Areas by UrbanBloom Potential Index")
    df = df.reset_index(drop=True)
    print(
        df[
            [
                "metro_area",
                "urbanbloom_index",
            ]
        ]
        .head(20)
        .to_string()
    )
    print("-" * 60)