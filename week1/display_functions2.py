import os  # For accessing and iterating over directory contents
import pandas as pd  # For data processing and handling CSV/TXT files
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For plotting visualizations
import seaborn as sns  # For enhanced visualization options

# Directory path for input data
input_dir = "../input/mitbih_database/"

# Helper function to read files and process the first 10 rows
def load_data(file_path, is_csv=True):
    """Reads the first 10 rows of a CSV or TXT file."""
    if is_csv:
        return pd.read_csv(file_path, nrows=10)
    else:
        return pd.read_csv(file_path, sep='\t', nrows=10)

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
        
        # Histogram
        plt.figure(figsize=(10, 6))
        df_csv.hist(bins=30, figsize=(10, 6))
        plt.suptitle(f"Histograms for {i}.csv")
        plt.show()
        
        # Correlation Matrix
        if df_csv.select_dtypes(include=[np.number]).shape[1] > 1:
            plt.figure(figsize=(8, 8))
            corr = df_csv.corr()
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
            plt.title(f"Correlation Matrix for {i}.csv")
            plt.show()

        # Scatter and Density Plot
        if df_csv.select_dtypes(include=[np.number]).shape[1] > 1:
            sns.pairplot(df_csv.select_dtypes(include=[np.number]))
            plt.suptitle(f"Scatter and Density Plots for {i}.csv", y=1.02)
            plt.show()

# Ensure proper resource handling for large datasets
