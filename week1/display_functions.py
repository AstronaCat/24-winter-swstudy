from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np  # Linear Algebra
import os           # Accessing directory structure
import pandas as pd # Data processing, CSV file I/O

# List files in the input directory
print(os.listdir('../input'))

# Read the CSV files into a pandas DataFrame
csv_file = '../input/mitbih_database/100.csv'
df_csv = pd.read_csv(csv_file)

# Read the TXT files into a pandas DataFrame
txt_file = '../input/mitbih_database/100annotations.txt'
df_txt = pd.read_csv(txt_file, sep='\t')

# Check whether the data is loaded correctly
print(df_csv.head())
print(df_txt.head())
print(df_csv.shape)
print(df_csv.columns)

# Histogram of column data
def plotHistogram(df, nHistogramShown, nHistogramPerRow):
    
    # Select only numeric columns for the histogram
    df_numeric = df.select_dtypes(include=[np.number])
    
    # Check if there are any numberic columns available
    if df_numeric.empty:
        print('NO numeric columns available')
        return
    
    # Count unique values in each numeric column
    nunique = df.nunique()

    # Filter columns based on the condition (1 < nunique < 50)
    df_filtered = df_numeric[[col for col in df_numeric if nunique[col]>1 and nunique[col]<50]]
    
    # Print the number of unique values and selected columns for debugging
    print(f'Number of unique values per columns: {nunique}')
    print(f'Columns selected for histogram: {df_filtered.columns}')
    
    # Get the shape of the filtered DataFrame
    nRow, nCol = df_filtered.shape
    if nCol==0:
        print('No columns selected for histogram')
        return
    
    # Prepare for plotting
    columnNames = list(df_filtered)
    nHistRow = (nCol + nHistogramPerRow - 1) / nHistogramPerRow
    
    # Create the plot
    plt.figure(num=None, figsize=(6 * nHistogramPerRow, 8 * nHistRow), dpi=80, facecolor='w', edgecolor='k')
    
    for i in range(min(nCol, nHistogramShown)):
        plt.subplot(nHistRow, nHistogramPerRow, i+1)
        df.iloc[:, i].hist()
        plt.ylabel('counts')
        plt.xticks(rotation=90)
        plt.title(f'{columnNames[i]} (column {i})')
    
    # Adjust layout and show plot
    plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
    plt.show()
    
    
    
# Correlation Matrix
def plotCorrelationMatrix(df, graphWidth):
    filename = '#100'
    df = df.dropna(axis=1)
    df = df[[col for col in df if df[col].nunique() > 1]]
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NAN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum=1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix for {filename}', fontsize=15)
    plt.show()



# Scatter and Density Plots
def plotScatterMatrix(df, plotSize, textSize):
    df = df.select_dtypes(include=[np.number])
    df = df.dropna(axis=1)
    df = df[[col for col in df if df[col].nunique()>1]]
    columnNames = list(df)
    if len(columnNames)>10:
        columnNames = columnNames[:10]
    
    df = df[columnNames]
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    
    for i, j in zip(*plt.np.triu_indices_from(ax, k=1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), 
                          xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()
  

# Plot histogram for CSV data
plotHistogram(df_csv, nHistogramShown=10, nHistogramPerRow=5)
# Plot histogram for TXT data
#plotHistogram(df_txt, nHistogramShown=10, nHistogramPerRow=5)

# Plot correlation matrix for CSV data
plotCorrelationMatrix(df_csv, graphWidth=10)
# Plot correlation matrix for TXT data
#plotCorrelationMatrix(df_txt, graphWidth=10)

# Plot scatter matrix for CSV data
plotScatterMatrix(df_csv, plotSize=10, textSize=10)
# Plot scatter matrix for TXT data
#plotScatterMatrix(df_txt, plotSize=10, textSize=10)

