import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Directory path for input data
input_dir = "../input/mitbih_database/"

# Load data function (provided by user)
def load_data(file_path, is_csv=True):
    """Reads the first 100 rows of a CSV or TXT file."""
    if is_csv:
        return pd.read_csv(file_path, nrows=100, header=None, names=["Time", "Lead1", "Lead2"])
    else:
        return pd.read_csv(
            file_path,
            sep='\s+',  # Updated to use sep='\s+' instead of delim_whitespace
            skiprows=1,  # Skip the header
            names=["Time", "Sample", "Type", "Sub", "Chan", "Num", "Aux"]
        )

# Function to plot waveform with annotations
def plot_waveform_with_annotations(df_csv, df_txt, record_id):
    """
    Plots the ECG waveform with annotations from the TXT file.
    
    Parameters:
    - df_csv: DataFrame containing the ECG data with columns ["Time", "Lead1", "Lead2"]
    - df_txt: DataFrame containing annotations with a "Time" column
    - record_id: Identifier for the record, used in the plot title
    """
    # Ensure Time column in df_csv is numeric
    df_csv["Time"] = pd.to_numeric(df_csv["Time"], errors='coerce')

    # Convert annotation times to seconds
    df_txt["Time"] = pd.to_datetime(df_txt["Time"], format='%M:%S.%f').apply(
        lambda x: x.minute * 60 + x.second + x.microsecond / 1e6)
    annotations = []

    # Find corresponding amplitude values for annotations in the CSV data
    for _, row in df_txt.iterrows():
        closest_idx = (df_csv["Time"] - row["Time"]).abs().idxmin()
        annotations.append({
            "Time": df_csv.loc[closest_idx, "Time"],
            "Amplitude": df_csv.loc[closest_idx, "Lead1"],
            "Amplitude2" : df_csv.loc[closest_idx, "Lead2"]
        })

    # Convert annotations to a DataFrame
    annotations_df = pd.DataFrame(annotations)

    # Plot waveform
    plt.figure(figsize=(10, 4))
    plt.plot(df_csv["Time"], df_csv["Lead1"], label="Lead1")
    plt.plot(df_csv["Time"], df_csv["Lead2"], label="Lead2", alpha=0.7)

    # Plot annotations as red dots
    if not annotations_df.empty:
        plt.scatter(
            annotations_df["Time"],
            annotations_df["Amplitude"],
            color="red",
            label="Event Annotations__Lead1",
            zorder=5
        )
        plt.scatter(
            annotations_df["Time"],
            annotations_df["Amplitude2"],
            color="blue",
            label="Event Annotations__Lead2",
            zorder=5
        )

    plt.title(f"ECG Waveform with Annotations for Record {record_id}")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    # Limit the number of ticks and format the labels
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=5))
    plt.gca().xaxis.set_tick_params(rotation=45)

    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Main execution
for i in range(100, 101):  # Limit to one file for simplicity; expand range as needed
    csv_file = os.path.join(input_dir, f"{i}.csv")
    txt_file = os.path.join(input_dir, f"{i}annotations.txt")

    # Check if files exist
    if os.path.exists(csv_file) and os.path.exists(txt_file):
        # Load CSV and TXT data using the provided load_data function
        df_csv = load_data(csv_file, is_csv=True)
        df_txt = load_data(txt_file, is_csv=False)

        # Ensure numeric types in CSV Time column
        df_csv["Time"] = pd.to_numeric(df_csv["Time"], errors='coerce')

        # Plot waveform with annotations
        print(f"Plotting waveform for record {i}")
        plot_waveform_with_annotations(df_csv, df_txt, record_id=i)
    else:
        print(f"Files missing for record {i}: {csv_file} or {txt_file}")