import pandas as pd
import numpy as np
from keras.models import load_model
import random as rand
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Specify the file name
file_name = BASE_DIR / 'base_stations_locations.csv'

csv_file_path = BASE_DIR / 'processed_data.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Get the third column (assuming 0-based indexing)
user_ids_column = df.iloc[:, 2]

Pos_BS_X = np.zeros(10)
Pos_BS_Y = np.zeros(10)
# Choose 10 unique user IDs randomly
random_BS_ids = rand.sample(user_ids_column.unique().tolist(), 10)

# Loop through each randomly selected user ID
BS_count = len(random_BS_ids) - 10

# Initialize an empty list to store data
BS_data = []

# Header row
BS_header = ['id_user', 'x_axis', 'y_axis']
BS_data.append(BS_header)

# 4
for selected_user_id in random_BS_ids:
    # Filter rows for the selected user ID and time slots 5, 6, 7, 8, 9
    selected_user_data = df[(df.iloc[:, 2] == selected_user_id) & (df.iloc[:, 5].isin([4]))]

    # Extract x-axis and y-axis values
    x_value = selected_user_data.iloc[:, 3]  # Assuming the fourth column is the x-axis
    y_value = selected_user_data.iloc[:, 4]  # Assuming the fifth column is the y-axis
    
    x_axis = x_value.tolist()
    y_axis = y_value.tolist()

    # print(f'Predicted x, y for new data: {new_predictions}')
    Pos_BS_X[BS_count] = x_axis[0]
    Pos_BS_Y[BS_count] = y_axis[0]

    # into CSV
    id_user = selected_user_id
    
    # Add the data for the current row
    row_data = [id_user, Pos_BS_X[BS_count], Pos_BS_Y[BS_count]]
    BS_data.append(row_data)

    BS_count = BS_count + 1

print(Pos_BS_X)    
print(Pos_BS_Y)

# Write data to CSV file
with open(file_name, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(BS_data)


