# Graph-Based Placement Heuristic

This module implements the selected 150-device, 10-edge-server placement experiment over five time slots (10–14). It reads the latest mobility predictions directly from `lstm_mobility_prediction/predicted_values.csv` and uses the fixed server coordinates in `base_stations_locations.csv`.

The implementation creates an undirected social graph from a randomly generated symmetric binary adjacency matrix, identifies connected components, and processes devices within each component as well as isolated devices. For each device, candidate servers are ranked by Euclidean distance from the device. A server is selected greedily when its remaining compute capacity is sufficient and the implemented latency expression is below the device's latency bound. Connected-component membership determines processing groups; it does not force all members of a component to use the same server.

The placement stage writes `dVariable.txt`, `DistSoc.txt`, and `Power_DV.txt`. The evaluation scripts consume these files to calculate total delay and energy. The social graph and transmission powers are generated randomly in the original implementation, so results can vary between runs. No random seed has been imposed by this cleanup because doing so would change the original experiment's stochastic behavior.
