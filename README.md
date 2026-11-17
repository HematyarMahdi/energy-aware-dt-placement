# Mobility-Aware Digital Twin Placement in Mobile Edge Computing

*Selected research code from my M.Sc. thesis in Computer Engineering*

## Overview

This repository presents selected Python implementations from my master's thesis research at **Iran University of Science and Technology (IUST)**. The research investigates mobility-aware, energy-conscious placement of digital twins (DTs) in **Mobile Edge Computing (MEC)** environments, where mobile devices, communication delays, and limited edge-server resources influence placement decisions.

The code shared here highlights two connected parts of the research: **LSTM-based mobility prediction** and a **graph-based placement heuristic**. It also includes selected scripts for evaluating delay and energy consumption.

## Selected Research Components

**1. LSTM-Based Mobility Prediction**  
A pre-trained LSTM model and its inference code estimate the future two-dimensional positions of mobile devices from sequences of historical observations. The selected implementation uses five observations per input sequence and produces predictions for five consecutive future time slots.

**2. Graph-Based Placement Heuristic**  
A heuristic for assigning mobile devices' digital twins to edge servers. It constructs an undirected graph of device relationships, identifies connected components to organize the allocation process, and greedily selects a nearby feasible server for each device subject to computational-capacity and latency constraints. Devices in the same connected component are not necessarily placed on the same server.

**3. Delay and Energy Evaluation**  
Selected scripts calculate delay- and energy-related metrics for the resulting placement decisions.

## Scope of This Repository

The shared material is a **curated subset of the thesis implementation**, rather than the complete thesis source code or a full experimental reproduction package. It includes a representative configuration with **150 mobile devices, 10 edge servers, and five time slots**, together with sample mobility data and the saved LSTM model. The LSTM training script and the complete set of thesis experiments are not included.

## Related Publication

Mahdi Hematyar and Zeinab Movahedi, **“Energy-Aware Dynamic Digital Twin Placement in Mobile Edge Computing,”** *2023 13th International Conference on Computer and Knowledge Engineering (ICCKE)*. [DOI: 10.1109/ICCKE60553.2023.10326254](https://doi.org/10.1109/ICCKE60553.2023.10326254)

**Author:** Mahdi Hematyar  
**Research area:** Digital Twins · Mobile Edge Computing · Mobility Prediction · Resource Allocation
