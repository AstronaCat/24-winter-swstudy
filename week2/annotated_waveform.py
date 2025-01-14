import os  # For accessing and iterating over directory contents
import pandas as pd  # For data processing and handling CSV/TXT files
import numpy as np  # For numerical operations

# Directory path for input data
input_dir = "../input/mitbih_database/"
output_dir = "../output/annotated_ecg_data/"
os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

# Helper function to read files and process the first 10 rows
def load_data(file_path, is_csv=True):
    """Reads the first 100 rows of a CSV or TXT file."""
    if is_csv:
        return pd.read_csv(file_path, nrows=100, header=None, names=["Time", "Lead1", "Lead2"])
    else:
        return pd.read_csv(
            file_path,
            delim_whitespace=True,
            skiprows=1,  # Skip the header
            names=["Time", "Sample", "Type", "Sub", "Chan", "Num", "Aux"]
        )

# for i in range(100, 235):
#     csv_file = os.path.join(input_dir, f"{i}.csv")
#     txt_file = os.path.join(input_dir, f"{i}annotations.txt")
    
#     # Check if files exist
#     if os.path.exists(csv_file) and os.path.exists(txt_file):
#         df_csv = load_data(csv_file)
#         df_txt = load_data(txt_file, is_csv=False)

#         # Print for debugging
#         print(f"Loaded {i}.csv and {i}annotations.txt")
#         print(df_csv.head())
#         print(df_txt.head())


# Helper function to annotate data
def annotate_data(df_csv, df_txt):
    """Annotates the CSV data using the TXT annotations."""
    df_txt["Time"] = df_txt["Time"].str.replace(":", ".").astype(float)  # Convert time format
    df_csv["Annotated"] = ""  # Initialize annotation column

    for _, row in df_txt.iterrows():
        closest_index = (df_csv["Time"] - row["Time"]).abs().idxmin()
        df_csv.loc[closest_index, "Annotated"] = row["Type"]  # Add annotation

    return df_csv

# Load and visualize files from 100 to 234
for i in range(100, 235):
    csv_file = os.path.join(input_dir, f"{i}.csv")
    txt_file = os.path.join(input_dir, f"{i}annotations.txt")
    output_file = os.path.join(output_dir, f"{i}_annotated.csv")

    # Check if files exist
    if os.path.exists(csv_file) and os.path.exists(txt_file):
        # Load CSV and TXT data
        df_csv = load_data(csv_file)
        df_txt = load_data(txt_file, is_csv=False)

        # Annotate data
        df_annotated = annotate_data(df_csv, df_txt)

        # Save annotated data
        df_annotated.to_csv(output_file, index=False)
        print(f"Annotated file saved to: {output_file}")

        # Plot waveform with annotations
        plt.figure(figsize=(10, 4))
        plt.plot(df_annotated["Time"], df_annotated["Lead1"], label="Lead1")
        plt.plot(df_annotated["Time"], df_annotated["Lead2"], label="Lead2")
        plt.scatter(
            df_annotated["Time"][df_annotated["Annotated"] != ""],
            df_annotated["Lead1"][df_annotated["Annotated"] != ""],
            color="red",
            label="Annotations",
            zorder=5,
        )
        plt.title(f"ECG Waveform with Annotations for {i}.csv")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.grid()
        plt.show()
    else:
        print(f"Files missing for record {i}: {csv_file} or {txt_file}")