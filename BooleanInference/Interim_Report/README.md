
# 🧬 booleansim.py - Boolean Network Simulator

This Python script simulates the dynamics of a Boolean Gene Regulatory Network (GRN) from a user-defined rule file. It runs simulations from random initial states and outputs state transition trajectories to analyze system dynamics such as steady states and limit cycles.

---

## 📁 Project Structure

```
.
├── booleansim.py          # Main simulation script
├── arb.txt                # Input file containing Boolean rules (1 per line)
├── state_transitions.csv  # Output file with all simulated state transitions
```

---

## ⚙️ Requirements

- Python 3.8+
- `pandas`
- `sympy`

Install dependencies:
```bash
pip install pandas sympy
```

---

## 📄 Input File Format (`arb.txt`)

Each line defines a Boolean rule:
```
GeneA = GeneB AND NOT GeneC
GeneB = GeneC OR GeneD
...
```

Use only `AND`, `OR`, and `NOT` (uppercase) for logic. The script automatically parses and converts these to symbolic form.

Example:
```txt
p53 = MDM2 AND NOT AKT
MDM2 = JNK OR p53
...
```

---

## 🚀 How to Run

```bash
python booleansim.py
```

The script will:
- Generate 1000 random initial states
- Simulate the Boolean network forward for up to 1000 steps per state
- Detect steady states or limit cycles
- Write transitions to `state_transitions.csv`
- Print progress and summary for each simulation

---

## 📤 Output

**`state_transitions.csv`** has two columns:
```
from_state,to_state
0010010110,0010011110
...
```

Each row is a transition from one network state to the next, represented as a bitstring (`0` or `1` per gene).

You’ll also see logs like:
```
🔎 Run 32/1000: steady state | steps = 12, cycle_length = 1
🔎 Run 33/1000: limit cycle | steps = 94, cycle_length = 4
```

---

## 🔎 Features

- Parallelized simulations for speed (using `ProcessPoolExecutor`)
- Automatic symbolic parsing of Boolean rules
- Support for fixed external inputs (e.g. `"TNF": 1`, `"GF": 1`)
- Tracks:
  - Simulation length
  - Limit cycles
  - Steady states

---

## 🧠 Next Steps

You can now:
- Use `state_transitions.csv` for **Boolean network inference**
- Identify **attractors** or **trap sets**
- Visualize the **state transition graph**
  

# 🧠 networkinference.py - Boolean Network Inference from Transition Data

This script learns Boolean update rules for each gene in a Boolean network using decision tree classifiers trained on simulated state transition data.

---

## 📁 Project Structure

```
.
├── infer_boolean_network.py  # This script
├── state_transitions.csv     # Input transition data (from previous simulation)
```

---

## ⚙️ Requirements

- Python 3.8+
- `pandas`
- `scikit-learn`

Install dependencies:
```bash
pip install pandas scikit-learn
```

---

## 📄 Input Format (`state_transitions.csv`)

This file must contain state transitions in the form:
```
from_state,to_state
010011001,010111001
...
```

Each row is a binary state transition (`0` or `1` per gene), encoded as strings.

---

## 🚀 How to Run

```bash
python infer_boolean_network.py
```

The script will:
- Load transitions from `state_transitions.csv`
- Treat each gene's next state as the learning target
- Train a decision tree for each gene
- Convert the tree to a human-readable Boolean expression
- Print all inferred rules

---

## 📤 Output

Example console output:
```
🧠 Inferred Boolean Network:

G0 = G26
G1 = G30
G2 = (G5 AND G25 AND G13 AND NOT G18 AND G3)
...
```

Each rule describes how the next state of a gene depends on the current state of others.

---

## 🔍 Features

- Learns Boolean logic without prior knowledge
- Supports any number of genes (based on bitstring length)
- Interpretable: rules shown in logical format
- Uses decision trees (bounded depth) for simplicity

---

## 🧠 Use Cases

- Reverse engineering gene regulatory networks
- Analyzing dynamics from simulations
- Exporting logic for modeling in `.bnet` or `.sif` formats
