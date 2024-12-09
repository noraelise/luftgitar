import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('../data_collection/data/air_guitar.csv')

# Print min and max for each feature
for column in data.columns:
    min_value = data[column].min()
    max_value = data[column].max()
    print(f"{column}: Min = {min_value}, Max = {max_value}")

# Plot histograms for the features
for column in data.columns:
    plt.figure(figsize=(8, 6))  # Set size for each histogram
    data[column].hist(bins=10, edgecolor='black')  # Adjust bins as needed
    plt.title(f"Histogram for {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.grid(False)  # Turn off grid if not needed
    plt.show()