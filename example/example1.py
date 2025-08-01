import pandas as pd
import os

from lib.file_ops import FileOps

# Static config
income_file = "Metro Area Dataset - Income by Metro Area.csv"
input_path = os.path.join(FileOps.get_input_path(), income_file)
output_path = os.path.join(FileOps.get_output_path(), "example1.xlsx")

def main():
    # Load dataset
    df = pd.read_csv(input_path)

    # Identify "<type> - Total" columns
    total_columns = [col for col in df.columns if col.strip().lower().endswith(" - total")]

    if not total_columns:
        raise ValueError("No columns matching '<type> - Total' found.")

    # Create new column: Area - Total
    df["Area - Total"] = df[total_columns].sum(axis=1)

    # Sort by Area - Total
    df_sorted = df.sort_values(by="Area - Total", ascending=ascend)

    # Keep only desired columns
    output_df = df_sorted[["Geographic Area Name", "Area - Total"]]

    # Export to Excel
    output_df.to_excel(output_path, index=False, engine='openpyxl')

    print(f"Output saved to: {output_path}")

if __name__ == "__main__":
    main()