import os  # For accessing and iterating over directory contents
import pandas as pd  # For data processing and handling CSV/TXT files
import numpy as np  # For numerical operations

# Directory path for input data
input_dir = "../input/mitbih_database/"
output_dir = "../output/annotated_ecg_data/"
os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

# Helper function to read files and process the first 10 rows
def load_data(file_path, is_csv=True):
    """Reads the first 10 rows of a CSV or TXT file."""
    if is_csv:
        return pd.read_csv(file_path, nrows=100)
    else:
        return pd.read_csv(file_path, sep='\t', nrows=100)

# Load and visualize files from 100 to 234
for i in range(100, 235):
    csv_file = os.path.join(input_dir, f"{i}.csv")
    txt_file = os.path.join(input_dir, f"{i}annotations.txt")
    
    # Check if files exist
    if os.path.exists(csv_file) and os.path.exists(txt_file):
        df_csv = load_data(csv_file)
        df_txt = load_data(txt_file, is_csv=False)

        # Print for debugging
        print(f"Loaded {i}.csv and {i}annotations.txt")
        print(df_csv.head())
        print(df_txt.head())