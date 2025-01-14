import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Directory path for input data
input_dir = "../input/mitbih_database/"

# Helper function to load CSV data
def load_csv(file_path, nrows=100):
    """Reads the first n rows of a CSV file."""
    df = pd.read_csv(file_path, nrows=nrows, header=None, names=["Time", "Lead1", "Lead2"])
    # If 'Time' is invalid or not numeric, use the index as a proxy for time
    if not pd.api.types.is_numeric_dtype(df["Time"]):
        df["Time"] = pd.to_numeric(df["Time"], errors='coerce')
    return df


# Function to plot waveform
def plot_waveform(df_csv, record_id):
    """Plots the ECG waveform."""
    plt.figure(figsize=(10, 4))
    plt.plot(df_csv["Time"], df_csv["Lead1"], label="Lead1")
    plt.plot(df_csv["Time"], df_csv["Lead2"], label="Lead2", alpha=0.7)
    
    plt.title(f"ECG Waveform for Record {record_id}")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    
    # Limit the number of ticks and format the labels
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))  # Max 10 ticks on x-axis
    plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=5))   # Max 5 ticks on y-axis
    plt.gca().xaxis.set_tick_params(rotation=45)             # Rotate x-axis labels if needed

    plt.legend()
    plt.grid()
    plt.tight_layout()  # Adjust layout to prevent label overlap
    plt.show()

# Load and visualize files from 100 to 234
for i in range(100, 235):
    csv_file = os.path.join(input_dir, f"{i}.csv")

    # Check if file exists
    if os.path.exists(csv_file):
        # Load CSV data
        df_csv = load_csv(csv_file)

        # Plot waveform
        print(f"Plotting waveform for record {i}")
        plot_waveform(df_csv, i)
    else:
        print(f"CSV file missing for record {i}: {csv_file}")
