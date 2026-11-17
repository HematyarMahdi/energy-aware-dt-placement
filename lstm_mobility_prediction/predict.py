import pandas as pd
import numpy as np
from keras.models import load_model
import random as rand
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Specify the file name
file_name = BASE_DIR / 'predicted_values.csv'

model = load_model(BASE_DIR / 'Final_Model_Last')

def create_sequences(data, sequence_length=5):
    sequences = []
    for i in range(len(data) - sequence_length + 1):
        sequence = data[i:i+sequence_length]
        sequences.append(sequence)
    return np.array(sequences)

sequence_length = 5

csv_file_path = BASE_DIR / 'processed_data.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Get the third column (assuming 0-based indexing)
user_ids_column = df.iloc[:, 2]

Pos_DV_X = np.zeros((5, 150))
Pos_DV_Y = np.zeros((5, 150))
# Choose 10 unique user IDs randomly
random_user_ids = rand.sample(user_ids_column.unique().tolist(), 150)

# Loop through each randomly selected user ID
count = len(random_user_ids) - 150

# Initialize an empty list to store data
data = []

# Header row
header = ['id_user', 'x_axis', 'y_axis', 'time_slot']
data.append(header)

# 5 - 9
for selected_user_id in random_user_ids:
    # Filter rows for the selected user ID and time slots 5, 6, 7, 8, 9
    selected_user_data = df[(df.iloc[:, 2] == selected_user_id) & (df.iloc[:, 5].isin([5, 6, 7, 8, 9]))]

    # Extract x-axis and y-axis values
    x_values = selected_user_data.iloc[:, 3]  # Assuming the fourth column is the x-axis
    y_values = selected_user_data.iloc[:, 4]  # Assuming the fifth column is the y-axis

    x_axis = x_values.tolist()
    y_axis = y_values.tolist()

    new_data = pd.DataFrame({'id_user': selected_user_id, 'timeslot': 10, 'x': [x_axis[0] , x_axis[1]  , x_axis[2] , x_axis[3] , x_axis[4]], 'y': [y_axis[0] , y_axis[1]  , y_axis[2] , y_axis[3] , y_axis[4]]})
    new_data_sequence = create_sequences(new_data, sequence_length)
    new_predictions = model.predict(new_data_sequence)


    print(f'Predicted x, y for new data: {new_predictions}')
    Pos_DV_X[0][count] = new_predictions[0][0]
    Pos_DV_Y[0][count] = new_predictions[0][1]

    # into CSV
    id_user = selected_user_id
    x_axis = new_predictions[0][0]
    y_axis = new_predictions[0][1]
    time_slot = 10

    # Add the data for the current row
    row_data = [id_user, x_axis, y_axis, time_slot]
    data.append(row_data)

    count = count + 1


count = len(random_user_ids) - 150
# 6 - 10
for selected_user_id in random_user_ids:
    # Filter rows for the selected user ID and time slots 6, 7, 8, 9, 10
    selected_user_data = df[(df.iloc[:, 2] == selected_user_id) & (df.iloc[:, 5].isin([6, 7, 8, 9, 10]))]

    # Extract x-axis and y-axis values
    x_values = selected_user_data.iloc[:, 3]  # Assuming the fourth column is the x-axis
    y_values = selected_user_data.iloc[:, 4]  # Assuming the fifth column is the y-axis

    x_axis = x_values.tolist()
    y_axis = y_values.tolist()

    new_data = pd.DataFrame({'id_user': selected_user_id, 'timeslot': 11, 'x': [x_axis[0] , x_axis[1]  , x_axis[2] , x_axis[3] , x_axis[4]], 'y': [y_axis[0] , y_axis[1]  , y_axis[2] , y_axis[3] , y_axis[4]]})
    new_data_sequence = create_sequences(new_data, sequence_length)
    new_predictions = model.predict(new_data_sequence)


    print(f'Predicted x, y for new data: {new_predictions}')
    Pos_DV_X[1][count] = new_predictions[0][0]
    Pos_DV_Y[1][count] = new_predictions[0][1]

    # into CSV
    id_user = selected_user_id
    x_axis = new_predictions[0][0]
    y_axis = new_predictions[0][1]
    time_slot = 11

    # Add the data for the current row
    row_data = [id_user, x_axis, y_axis, time_slot]
    data.append(row_data)

    count = count + 1

count = len(random_user_ids) - 150
# 7 - 11
for selected_user_id in random_user_ids:
    # Filter rows for the selected user ID and time slots 7, 8, 9, 10, 11
    selected_user_data = df[(df.iloc[:, 2] == selected_user_id) & (df.iloc[:, 5].isin([7, 8, 9, 10, 11]))]

    # Extract x-axis and y-axis values
    x_values = selected_user_data.iloc[:, 3]  # Assuming the fourth column is the x-axis
    y_values = selected_user_data.iloc[:, 4]  # Assuming the fifth column is the y-axis

    x_axis = x_values.tolist()
    y_axis = y_values.tolist()

    new_data = pd.DataFrame({'id_user': selected_user_id, 'timeslot': 12, 'x': [x_axis[0] , x_axis[1]  , x_axis[2] , x_axis[3] , x_axis[4]], 'y': [y_axis[0] , y_axis[1]  , y_axis[2] , y_axis[3] , y_axis[4]]})
    new_data_sequence = create_sequences(new_data, sequence_length)
    new_predictions = model.predict(new_data_sequence)


    print(f'Predicted x, y for new data: {new_predictions}')
    Pos_DV_X[2][count] = new_predictions[0][0]
    Pos_DV_Y[2][count] = new_predictions[0][1]

    # into CSV
    id_user = selected_user_id
    x_axis = new_predictions[0][0]
    y_axis = new_predictions[0][1]
    time_slot = 12

    # Add the data for the current row
    row_data = [id_user, x_axis, y_axis, time_slot]
    data.append(row_data)

    count = count + 1

count = len(random_user_ids) - 150
# 8 - 12
for selected_user_id in random_user_ids:
    # Filter rows for the selected user ID and time slots 8, 9, 10, 11, 12
    selected_user_data = df[(df.iloc[:, 2] == selected_user_id) & (df.iloc[:, 5].isin([8, 9, 10, 11, 12]))]

    # Extract x-axis and y-axis values
    x_values = selected_user_data.iloc[:, 3]  # Assuming the fourth column is the x-axis
    y_values = selected_user_data.iloc[:, 4]  # Assuming the fifth column is the y-axis

    x_axis = x_values.tolist()
    y_axis = y_values.tolist()

    new_data = pd.DataFrame({'id_user': selected_user_id, 'timeslot': 13, 'x': [x_axis[0] , x_axis[1]  , x_axis[2] , x_axis[3] , x_axis[4]], 'y': [y_axis[0] , y_axis[1]  , y_axis[2] , y_axis[3] , y_axis[4]]})
    new_data_sequence = create_sequences(new_data, sequence_length)
    new_predictions = model.predict(new_data_sequence)


    print(f'Predicted x, y for new data: {new_predictions}')
    Pos_DV_X[3][count] = new_predictions[0][0]
    Pos_DV_Y[3][count] = new_predictions[0][1]

    # into CSV
    id_user = selected_user_id
    x_axis = new_predictions[0][0]
    y_axis = new_predictions[0][1]
    time_slot = 13

    # Add the data for the current row
    row_data = [id_user, x_axis, y_axis, time_slot]
    data.append(row_data)

    count = count + 1 

count = len(random_user_ids) - 150
# 9 - 13
for selected_user_id in random_user_ids:
    # Filter rows for the selected user ID and time slots 9, 10, 11, 12, 13
    selected_user_data = df[(df.iloc[:, 2] == selected_user_id) & (df.iloc[:, 5].isin([9, 10, 11, 12, 13]))]

    # Extract x-axis and y-axis values
    x_values = selected_user_data.iloc[:, 3]  # Assuming the fourth column is the x-axis
    y_values = selected_user_data.iloc[:, 4]  # Assuming the fifth column is the y-axis

    x_axis = x_values.tolist()
    y_axis = y_values.tolist()

    new_data = pd.DataFrame({'id_user': selected_user_id, 'timeslot': 14, 'x': [x_axis[0] , x_axis[1]  , x_axis[2] , x_axis[3] , x_axis[4]], 'y': [y_axis[0] , y_axis[1]  , y_axis[2] , y_axis[3] , y_axis[4]]})
    new_data_sequence = create_sequences(new_data, sequence_length)
    new_predictions = model.predict(new_data_sequence)


    print(f'Predicted x, y for new data: {new_predictions}')
    Pos_DV_X[4][count] = new_predictions[0][0]
    Pos_DV_Y[4][count] = new_predictions[0][1]

    # into CSV
    id_user = selected_user_id
    x_axis = new_predictions[0][0]
    y_axis = new_predictions[0][1]
    time_slot = 14

    # Add the data for the current row
    row_data = [id_user, x_axis, y_axis, time_slot]
    data.append(row_data)

    count = count + 1        

# Write data to CSV file
with open(file_name, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(data)

print(Pos_DV_X)
print(Pos_DV_Y)

    # print(f"User ID: {selected_user_id}")
    # print("X-axis values:", x_values.tolist())
    # print("Y-axis values:", y_values.tolist())

# print(random_user_ids)

# Choose the first randomly selected user ID
# selected_user_id = random_user_ids[0]

# Filter rows for the selected user ID and time slots 5, 6, 7, 8, 9
# selected_user_data = df[(df.iloc[:, 2] == selected_user_id) & (df.iloc[:, 5].isin([5, 6, 7, 8, 9]))]

# Extract x-axis and y-axis values
# x_values = selected_user_data.iloc[:, 3]  # Assuming the fourth column is the x-axis
# y_values = selected_user_data.iloc[:, 4]  # Assuming the fifth column is the y-axis

# print(f"User ID: {selected_user_id}")
# print("X-axis values:", x_values.tolist())
# print("Y-axis values:", y_values.tolist())









# ---------------------
# Pos_DV_X = np.zeros((5, 10))
# Pos_DV_Y = np.zeros((5, 10))

# device_count = 0
# timeslot_count = 0
# # Loop through the time_slot values
# for time_slot_value in time_slots_to_check:
#     # Filter the DataFrame based on the current time_slot value
#     filtered_data = df[df['time_slot'] == time_slot_value]

#     # Extract x_axis and y_axis values from the filtered data
#     x_values = filtered_data['x_axis'].tolist()
#     y_values = filtered_data['y_axis'].tolist()
#     Pos_DV_X[timeslot_count] = x_values
#     Pos_DV_Y[timeslot_count] = y_values
#     timeslot_count = timeslot_count + 1
# ---------------------


