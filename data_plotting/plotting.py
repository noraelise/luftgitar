import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('../data_collection/data/air_guitar.csv')

# Print min and max for each feature
for column in data.columns:
    min_value = data[column].min()
    max_value = data[column].max()
    print(f"{column}: Min = {min_value}, Max = {max_value}")

# Plot histograms for the features
num_columns = data.columns
data[num_columns].hist(bins=10, figsize=(15, 10))  # Adjust bins and figsize as needed
plt.suptitle("Histograms for Each Feature")
plt.show()
