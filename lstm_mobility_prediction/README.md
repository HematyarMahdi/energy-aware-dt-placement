# LSTM-Based Mobility Prediction

This module performs inference with the pre-trained TensorFlow/Keras SavedModel in `Final_Model_Last/`. It uses five consecutive observations and four input features (`id_user`, `timeslot`, `x`, and `y`) to predict the next two-dimensional position (`x`, `y`). The inference script applies this one-step-ahead prediction to five consecutive windows, producing positions for time slots 10–14.

The included `processed_data.csv` is a compact sample containing 150 device IDs and the historical time slots needed by the selected experiment. The script writes `predicted_values.csv`, which is consumed directly by the graph-based placement module.

The supplied thesis-code archive contains the trained model and inference code, but does not include the model-training script. `select_base_stations.py` is an auxiliary utility for selecting ten base-station locations from the time-slot-4 observations; the selected experiment's fixed base-station coordinates are stored in the graph module.
