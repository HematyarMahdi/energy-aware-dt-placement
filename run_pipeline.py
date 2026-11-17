"""Run the archived LSTM inference, graph placement, and metric evaluation."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
LSTM_DIR = ROOT / "lstm_mobility_prediction"
GRAPH_DIR = ROOT / "graph_based_heuristic"
STEPS = [
    ("LSTM mobility prediction", LSTM_DIR / "predict.py", LSTM_DIR),
    ("Graph-based placement", GRAPH_DIR / "placement.py", GRAPH_DIR),
    ("Delay evaluation", GRAPH_DIR / "evaluation" / "delay_calculation.py", GRAPH_DIR),
    ("Energy evaluation", GRAPH_DIR / "evaluation" / "energy_calculation.py", GRAPH_DIR),
]

for label, script, working_directory in STEPS:
    print(f"\n=== {label} ===", flush=True)
    subprocess.run([sys.executable, str(script)], cwd=working_directory, check=True)

print("\nPipeline completed. See graph_based_heuristic/myTotalDelay.txt and myEnergy.txt.")
