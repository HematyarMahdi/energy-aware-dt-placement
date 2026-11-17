import math
import networkx as nx
import numpy as np
import pandas as pd
import random
import csv
from pathlib import Path

GRAPH_DIR = Path(__file__).resolve().parent
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

# print(Pos_DV_X)
# print(Pos_DV_Y)
    
# Specify the rows and columns you want to read
# rows_to_read_SDV = 13  # Number of rows to read
# Number of IoT Devices
nbSDV =  150
SDV = range(nbSDV)

# column1_index = 0  # Index of the first column (0-based index)
# column2_index = 1  # Index of the second column (0-based index)
# column3_index = 2

# df_SDV = pd.read_csv(csv_file, usecols=[column1_index, column2_index], nrows=10)

# Pos_DV_X = df_SDV.iloc[:, 0].tolist()   # 1D Array
# Pos_DV_Y = df_SDV.iloc[:, 1].tolist()
# print(Pos_DV_X)

BS_csv_file_path = GRAPH_DIR / 'base_stations_locations.csv'
BS_df = pd.read_csv(BS_csv_file_path, header=None, names=['id_user', 'x_axis', 'y_axis'])

Pos_BS_X = np.zeros(10)
Pos_BS_Y = np.zeros(10)

# rows_to_read_Server = 7
# Number of Servers
nbServers = 10
Servers = range(nbServers)
# df_Server = pd.read_csv(csv_file, skiprows=70, usecols=[column1_index, column2_index, column3_index], nrows=rows_to_read_Server)

Pos_BS_X = BS_df.iloc[:, 1].tolist()
Pos_BS_Y = BS_df.iloc[:, 2].tolist()

# print(Pos_BS_X)
# print(Pos_BS_Y)

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
# Power_DV = np.zeros((nbSlots, nbSDV)) # 1 W --> Max
# Power_DV = [
#  	[0.5, 0.6, 0.5, 0.6, 0.8, 0.4, 0.6, 0.6, 0.4, 0.7, 0.4, 0.6, 0.5],
#  	[0.3, 0.5, 0.5, 0.5, 0.8, 0.5, 0.8, 0.5, 0.8, 0.7, 0.6, 0.8, 0.6],
#  	[0.8, 0.3, 0.8, 0.8, 0.6, 0.8, 0.4, 0.8, 0.8, 0.7, 0.4, 0.5, 0.5]
# ]; 
# Power_DV2 = np.random.rand(3, 13)
Power_DV2 = np.random.uniform(low=0.29, high=0.8, size=(nbSlots, nbSDV))
Power_DV = np.round(Power_DV2, decimals=1)
# print('The First: ', Power_DV)
# print('----------')
print('Power DV: ', Power_DV)

#Variance = ...; # 10^-12 W
Bandwidth = 20 # 1 MGH
Rate = np.zeros((nbSlots, nbSDV))

# Data_Size = np.zeros((nbSlots, nbSDV))
# Data_Size = [
# 	[500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500],
# 	[500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500],
# 	[500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500],
# ];
Data_Size = np.full((nbSlots, nbSDV), 500)

Off_Latency = np.zeros((nbSlots, nbSDV))

Dist_DV_Near = np.zeros((nbSlots, nbSDV)) 

#float base;

# Total Frequency of Edge Servers
TotalFrequency = np.full(nbServers, 5000)
# TotalFrequency = [800, 800]
TotalFrequencyInitial = np.full(nbServers, 5000)

# Frequency Demand for each IoT Device
#Freq = [700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700]
Freq = np.full(nbSDV, 700)

# Maximum Latency for each IoT Device
# Lmax = [1, 0.92, 0.98, 1, 0.91, 1, 1, 0.96, 0.998, 0.93, 0.95, 0.95, 0.95]
Lmax = np.full(nbSDV, 1.8)
print(Lmax)

# Distance between IoT Devices and Edge Servers during each Time Slot
DistCost = np.zeros((nbSlots, nbSDV, nbServers))

detta = 3.33

# Social Connection Status between each two IoT Devices
# Initialize DistSoc as a list of lists filled with zeros
# DistSoc = [[0 for _ in range(nbSDV)] for _ in range(nbSDV)]

# Input values for each pair of devices
# for i in range(nbSDV):
#     for j in range(nbSDV):        
#         probability = int(input(f"Enter probability of data exchange between Device {i} and Device {j}: "))
#         DistSoc[i][j] = probability

# DistSoc =  [
#     [0,1,1,0,0,1,1,0,1,1,1,1,0],
#     [1,0,1,0,0,0,1,0,0,1,0,0,0],
#     [1,0,0,1,1,1,0,0,0,0,1,1,0],
#     [1,0,0,0,0,1,0,1,1,0,1,1,0],
#     [1,0,1,0,0,1,0,0,0,1,1,0,0],
#     [1,1,1,0,1,0,0,1,1,0,1,0,0],
#     [1,0,1,0,0,0,0,0,1,1,0,1,0],
#     [1,0,0,1,1,0,0,0,1,1,0,1,0],
#     [1,0,1,1,0,0,0,1,0,1,1,0,0],
#     [1,0,1,1,0,1,1,0,1,0,0,0,0],
#     [1,0,1,1,0,1,1,0,1,0,0,0,0],
#     [1,0,1,1,0,1,1,0,1,0,0,0,0],
#     [1,0,1,1,0,1,1,0,1,0,0,0,0]
# ]
DistSoc2 = np.random.choice([0, 1], size=(nbSDV, nbSDV))
DistSoc = np.triu(DistSoc2) + np.triu(DistSoc2, k=1).T
print(DistSoc)
# print('DistSoc is: ', DisSoc2)

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

# print(Second_Array)
# print(PP)
# print(Pos_N_Y)
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
        #Rate[t][i] = Bandwidth * Math.log(1 + (Power_DV[t][i] * Gain_DV_Near[t][i]/(Variance * Variance)));
        # Rate[t][i] = 20 * math.log(1 + (Power_DV[t][i] * Gain_DV_Near[t][i]/(math.pow(10, -12))))/math.log(2)        
        Rate[t][i] = 20 * math.log10(1 + (Power_DV[t][i] * Gain_DV_Near[t][i])/math.pow(10, -24))

print("Rate is: ",Rate)
for t in Slots:
    for i in SDV:
        Off_Latency[t][i] = Data_Size[t][i]/Rate[t][i]; 		

print("Offloading latency is: ",Off_Latency)
# Create an empty graph
GP = nx.Graph()     # Pass

# Add vertices to the graph
GP.add_nodes_from(range(nbSDV))  # Pass

# Add weighted edges to the graph
# Iterate through the 2D array and add weighted edges to the graph
for i in range(len(DistSoc)):
    for j in range(i + 1, len(DistSoc[i])):
        if DistSoc[i][j] == 1:
            GP.add_edge(i, j, weight=1)

# Create an empty graph
GS = nx.Graph()     # Pass

# Add vertices to the graph
GS.add_nodes_from(range(nbServers))     # Pass

dVariable = np.zeros((nbSlots, nbSDV, nbServers))

def generate_mappings(GP_prime, not_connected, VS):
    # Randomly generate initial mappings for devices and servers
    # array_of_dicts = [
    #     {},
    #     {},
    #     {},
    #     {},
    #     {}
    # ]
    counttt = 0
    for timeslot in range(nbSlots):
        mapping = {}
        # At the begining of each time slot, the total frequency of servers will be released
        for server in range(nbServers):
            TotalFrequency[server] = TotalFrequencyInitial[server]
        for component in GP_prime:
            for device in list(component):
                near = np.zeros(nbServers)
                for ss in range(nbServers):
                    near[ss] = distance(Pos_DV_X[timeslot][device], Pos_DV_Y[timeslot][device], Pos_BS_X[ss], Pos_BS_Y[ss])
                index_element_pairs = list(enumerate(near))
                sorted_pairs = sorted(index_element_pairs, key=lambda x: x[1])
                sorted_indices = [pair[0] for pair in sorted_pairs]
                # print(sorted_indices)
                for server in sorted_indices:  
                    # print(server)          
                    print('Total Latency is: ',(DistCost[timeslot][device][server] + Off_Latency[timeslot][device]))
                    if (Freq[device] <= TotalFrequency[server] and ((DistCost[timeslot][device][server] + Off_Latency[timeslot][device]) < Lmax[device])):
                        # server = random.choice(VS.nodes())  # Randomly assign a server to each device
                        TotalFrequency[server] = TotalFrequency[server] - Freq[device]    
                        # array_of_dicts[timeslot][device] = server                   
                        mapping[device] = server
                        dVariable[timeslot][device][server] = 1
                        counttt = counttt + 1
                        break
        for device in not_connected:            
            near = np.zeros(nbServers)
            for ss in range(nbServers):
                near[ss] = distance(Pos_DV_X[timeslot][device], Pos_DV_Y[timeslot][device], Pos_BS_X[ss], Pos_BS_Y[ss])
            index_element_pairs = list(enumerate(near))
            sorted_pairs = sorted(index_element_pairs, key=lambda x: x[1])
            sorted_indices = [pair[0] for pair in sorted_pairs]
            for server in sorted_indices:            
                if (Freq[device] <= TotalFrequency[server] and ((DistCost[timeslot][device][server] + Off_Latency[timeslot][device]) < Lmax[device])):
                    # server = random.choice(VS.nodes())  # Randomly assign a server to each device
                    TotalFrequency[server] = TotalFrequency[server] - Freq[device]    
                    # array_of_dicts[timeslot][device] = server                   
                    mapping[device] = server
                    dVariable[timeslot][device][server] = 1
                    break
            # for server in range(nbServers):            
            #     if (Freq[device] <= TotalFrequency[server] and (DistCost[timeslot][device][server] + Off_Latency[timeslot][device]) < Lmax[device]):
            #         # server = random.choice(VS.nodes())  # Randomly assign a server to each device
            #         TotalFrequency[server] = TotalFrequency[server] - Freq[device]   
            #         # array_of_dicts[timeslot][device] = server                         
            #         mapping[device] = server
            #         dVariable[timeslot][device][server] = 1
            #         break
        # print(mapping)
    # print(dVariable)
    # print(750 - counttt)

    np.savetxt(GRAPH_DIR / 'dVariable.txt', dVariable.flatten(), fmt='%d', delimiter=', ')

    np.savetxt(GRAPH_DIR / 'DistSoc.txt', DistSoc.flatten(), fmt='%d', delimiter=', ')


    np.savetxt(GRAPH_DIR / 'Power_DV.txt', Power_DV.flatten(), fmt='%.1f', delimiter=', ')



    # Specify the CSV file name
    # dVariable_csv_file = 'my_dVariable.csv'

    # Writing to CSV file
    # with open(dVariable_csv_file, 'w', newline='') as file:
        # writer = csv.writer(file)
        
        # Write the header if needed
        # writer.writerow(['ID', 'Name', 'Age'])
        
        # Write the data
        # writer.writerows(dVariable)
    # print(array_of_dicts)

    return mapping

def graph_based_heuristic():
    GP = nx.Graph()
    GP.add_nodes_from(range(nbSDV))
    for i in range(len(DistSoc)):
        for j in range(i + 1, len(DistSoc[i])):
            if DistSoc[i][j] == 1:
                GP.add_edge(i, j, weight=1)
    # VP = GP.nodes()
    VS = GS.nodes()
    # GP_prime = find_connected_components(GP)
    GP_prime = []

    subgraphs = list(nx.connected_components(GP))
    print(subgraphs)
    for subgraph in subgraphs:
        if len(subgraph) != 1:
            GP_prime.append(subgraph)    

    print(GP_prime)
    not_subgraphs = []
    for subgraph in subgraphs:
        if len(subgraph) == 1:
            not_subgraphs.append(subgraph) 

    # result = [item for subset in GP_prime for item in subset]
    int_list = [int(list(item)[0]) for item in not_subgraphs]
    print(int_list)

    mapping = generate_mappings(GP_prime, int_list, VS)
    
    return mapping   

if __name__ == '__main__':
    graph_based_heuristic()