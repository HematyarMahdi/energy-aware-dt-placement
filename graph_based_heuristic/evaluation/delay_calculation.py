import math
import networkx as nx
import numpy as np
import pandas as pd
import random
import csv
from pathlib import Path

GRAPH_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = GRAPH_DIR.parent

csv_file_path = REPO_ROOT / 'lstm_mobility_prediction' / 'predicted_values.csv'
df = pd.read_csv(csv_file_path)
time_slots_to_check = [10, 11, 12, 13, 14]

Pos_DV_X = np.zeros((5, 150))
Pos_DV_Y = np.zeros((5, 150))

device_count = 0
timeslot_count = 0
# Loop through the time_slot values
for time_slot_value in time_slots_to_check:
    # Filter the DataFrame based on the current time_slot value
    filtered_data = df[df['time_slot'] == time_slot_value]

    # Extract x_axis and y_axis values from the filtered data
    x_values = filtered_data['x_axis'].tolist()
    y_values = filtered_data['y_axis'].tolist()
    Pos_DV_X[timeslot_count] = x_values
    Pos_DV_Y[timeslot_count] = y_values

    timeslot_count = timeslot_count + 1

# Number of IoT Devices
nbSDV =  150
SDV = range(nbSDV)

BS_csv_file_path = GRAPH_DIR / 'base_stations_locations.csv'
BS_df = pd.read_csv(BS_csv_file_path, header=None, names=['id_user', 'x_axis', 'y_axis'])

Pos_BS_X = np.zeros(10)
Pos_BS_Y = np.zeros(10)

# Number of Servers
nbServers = 10
Servers = range(nbServers)

Pos_BS_X = BS_df.iloc[:, 1].tolist()
Pos_BS_Y = BS_df.iloc[:, 2].tolist()

# Number of Time Slots
nbSlots = 5     # 10, 11, 12, 13, 14
Slots = range(nbSlots)

Pos_N_X = np.zeros((nbSlots, nbSDV))
Pos_N_Y = np.zeros((nbSlots, nbSDV))

# Number of Device type
nbTypes = 8

# g_zero = 0.0001 # Wat 
g_zero = 1
d_zero = 1

Gain_DV_Near = np.zeros((nbSlots, nbSDV))  # Channel gain

# transmission power
# Power_DV2 = np.random.uniform(low=0.29, high=0.8, size=(nbSlots, nbSDV))
# Power_DV = np.round(Power_DV2, decimals=1)

Power_DV = np.loadtxt(GRAPH_DIR / 'Power_DV.txt', delimiter=',', dtype=float)
# Reshape to the original array shape
loaded_Power_DV = (nbSlots, nbSDV)  # Replace this with the actual shape of your original array
Power_DV = Power_DV.reshape(loaded_Power_DV)
print('Power DV: ', Power_DV)

Bandwidth = 20 # 1 MGH
Rate = np.zeros((nbSlots, nbSDV))

Data_Size = np.full((nbSlots, nbSDV), 500)

Off_Latency = np.zeros((nbSlots, nbSDV))

Dist_DV_Near = np.zeros((nbSlots, nbSDV)) 

# Total Frequency of Edge Servers
TotalFrequency = np.full(nbServers, 5000)
# TotalFrequency = [800, 800]
TotalFrequencyInitial = np.full(nbServers, 5000)

Freq = np.full(nbSDV, 700)

Lmax = np.full(nbSDV, 1.8)

# Distance between IoT Devices and Edge Servers during each Time Slot
DistCost = np.zeros((nbSlots, nbSDV, nbServers))

detta = 3.33

# Social Connection Status between each two IoT Devices
# Initialize DistSoc as a list of lists filled with zeros
# DistSoc2 = np.random.choice([0, 1], size=(nbSDV, nbSDV))
# DistSoc = np.triu(DistSoc2) + np.triu(DistSoc2, k=1).T
# print('DistSoc is: ', DistSoc)
# print('DistSoc is: ', DisSoc2)

DistSoc = np.loadtxt(GRAPH_DIR / 'DistSoc.txt', delimiter=',', dtype=int)
# Reshape to the original array shape
loaded_DistSoc = (nbSDV, nbSDV)  # Replace this with the actual shape of your original array
DistSoc = DistSoc.reshape(loaded_DistSoc)
print(DistSoc)

def distance(first_X, first_Y, Second_X, Second_Y):
    return math.sqrt(math.pow((Second_X - first_X),2) + math.pow((Second_Y - first_Y),2))

base_stations = [(x, y) for x, y in zip(Pos_BS_X, Pos_BS_Y)]
for t in Slots:
    for i in SDV:
        min_distance = float('inf')  # Set initial minimum distance to a large value
        min_bs_index = None  # Variable to store the index of the closest base station
        
        # Calculate distance for each base station and find the closest one
        for bs_index, (bs_x, bs_y) in enumerate(base_stations):
            dv_distance = distance(Pos_DV_X[t][i], Pos_DV_Y[t][i], bs_x, bs_y)
            if dv_distance < min_distance:
                min_distance = dv_distance
                min_bs_index = bs_index
        
        # Set Pos_N_X and Pos_N_Y based on the closest base station
        Pos_N_X[t][i], Pos_N_Y[t][i] = base_stations[min_bs_index]


for t in Slots:
    for i in SDV:
        for k in Servers:
            DistCost[t][i][k] = detta * distance(Pos_N_X[t][i], Pos_N_Y[t][i], Pos_BS_X[k], Pos_BS_Y[k])	

for t in Slots:
 	for i in SDV:
 			# The distance between IoT device and it's nearest base station
 		Dist_DV_Near[t][i] = distance(Pos_N_X[t][i], Pos_N_Y[t][i], Pos_DV_X[t][i], Pos_DV_Y[t][i])		 		
# print(Dist_DV_Near)

for t in Slots:
    for i in SDV:
        base = (d_zero/Dist_DV_Near[t][i]); 		 		
        Gain_DV_Near[t][i] = g_zero * (math.pow(base, 4))	 # Wat/Km	

# print(Gain_DV_Near)
for t in Slots:
    for i in SDV:      
        Rate[t][i] = 20 * math.log10(1 + (Power_DV[t][i] * Gain_DV_Near[t][i])/math.pow(10, -24))

print("Rate is: ",Rate)
for t in Slots:
    for i in SDV:
        Off_Latency[t][i] = Data_Size[t][i]/Rate[t][i]; 		

print("Offloading latency is: ",Off_Latency)    

# Specify the CSV file name
# dVariable_csv_file = 'my_dVariable.csv'
# Reading from CSV file using pandas
# dVaribale_df = pd.read_csv(dVariable_csv_file)
# print(dVaribale_df)

# dVariable = np.zeros((nbSlots, nbSDV, nbServers))
# Iterate through rows
# time_count = 0
# device_count = 0
# for index, row in dVaribale_df.iterrows():
#     for column in row:
#         dVariable[time_count][device_count] = float(column)
#         device_count = device_count + 1
#     device_count = 0
#     time_count = time_count + 1
loaded_data = np.loadtxt(GRAPH_DIR / 'dVariable.txt', delimiter=',', dtype=int)
# Reshape to the original array shape
dVariable = (nbSlots, nbSDV, nbServers)  # Replace this with the actual shape of your original array
loaded_data = loaded_data.reshape(dVariable)
# print(loaded_data)
    
# dVariable = dVaribale_df.to_numpy()    
# Iterate through the DataFrame and fill the numpy array        

def delay_calculation(loaded_data):
    file_path = GRAPH_DIR / 'myTotalDelay.txt'
    # Open the file in write mode and redirect the standard output to the file
    with open(file_path, 'w') as file:            
        totalDelay = 0
        for time_slot in range(nbSlots):
            for device in range(nbSDV):
                for server in range(nbServers):
                    totalDelay = totalDelay + (loaded_data[time_slot][device][server] * (DistCost[time_slot][device][server] + Off_Latency[time_slot][device]))
                #print('device: ', device, ' timeslot: ', time_slot, ' total delay: ', totalDelay)
        # Use the print statement to write to the file        
        print('total delay: ', totalDelay, file=file)
    return totalDelay

# print(delay_calculation(loaded_data))
delay_calculation(loaded_data)