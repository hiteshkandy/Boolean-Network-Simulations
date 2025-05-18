import itertools
import pandas as pd
import sympy as sp
import re
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv

# --- Load and parse the rules ---
with open("/Users/hiteshkandarpa/Desktop/Acads/AlgoBio/Project/Code/Network Simulations/arb.txt", "r") as file:
    lines = file.readlines()

rules = [line.strip() for line in lines if '=' in line]
rules_dict = {}
for rule in rules:
    var, expr = rule.split('=', 1)
    var = var.strip()
    expr = expr.strip()
    expr = expr.replace('AND', '&').replace('OR', '|').replace('NOT', '~')
    expr = re.sub(r'\b(\w+)\b', r'symbols["\1"]', expr)
    rules_dict[var] = expr

# --- Extract all variable names (LHS + RHS) ---
all_names = set(rules_dict.keys())
for expr in rules_dict.values():
    tokens = re.findall(r'symbols\["(\w+)"\]', expr)
    all_names.update(tokens)

# Create sympy symbols for all variables
symbols = {name: sp.Symbol(name) for name in all_names}

# Compile sympy Boolean expressions
update_funcs = {
    node: sp.sympify(expr, locals={'symbols': symbols})
    for node, expr in rules_dict.items()
}

# --- Fix external inputs ---
fixed_nodes = {
    "TNF": 1,
    "GF": 1
}
node_names = sorted(list(symbols.keys()))
non_fixed_nodes = [n for n in node_names if n not in fixed_nodes]

# --- Create helper maps ---
idx2node = {i: node for i, node in enumerate(node_names)}
node2idx = {node: i for i, node in idx2node.items()}

# --- Utility functions ---
def state_to_str(state):
    return ''.join(str(b) for b in state)

def next_state(current_state):
    env = {symbols[node]: current_state[node2idx[node]] for node in node_names}
    next_state = []
    for node in node_names:
        if node in fixed_nodes:
            next_state.append(fixed_nodes[node])
        elif node in update_funcs:
            val = int(bool(update_funcs[node].subs(env)))
            next_state.append(val)
        else:
            next_state.append(current_state[node2idx[node]])
    return tuple(next_state)

# --- Generate random initial states ---
num_samples = 1000
initial_states = []
for _ in range(num_samples):
    state = [0] * len(node_names)
    for i, node in enumerate(node_names):
        if node in fixed_nodes:
            state[i] = fixed_nodes[node]
        else:
            state[i] = random.randint(0, 1)
    initial_states.append(tuple(state))

# --- Simulation function for each process ---
def simulate_from_initial(init):
    visited = []
    current = init
    transitions_local = []
    status = "unknown"
    cycle_length = 0

    for step in range(1000):
        current_str = state_to_str(current)
        if current_str in visited:
            idx = visited.index(current_str)
            if idx == len(visited) - 1:
                status = "steady state"
                cycle_length = 1
            else:
                status = "limit cycle"
                cycle_length = len(visited) - idx
            break
        visited.append(current_str)
        nxt = next_state(current)
        transitions_local.append((current_str, state_to_str(nxt)))
        current = nxt

    if status == "unknown":
        status = "max steps reached"

    result = {
        "transitions": transitions_local,
        "status": status,
        "cycle_length": cycle_length,
        "steps": len(transitions_local)
    }
    return result

# --- Main execution block ---
if __name__ == "__main__":
    output_file = "state_transitions.csv"
    print(f"📂 Writing to {output_file}...")

    # Create file and write header
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["from_state", "to_state"])

    print("🚀 Starting parallel simulation...")

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(simulate_from_initial, init) for init in initial_states]

        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()

            # Append transitions to file
            with open(output_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(result["transitions"])

            # Print run summary
            print(f"🔎 Run {i}/{num_samples}: {result['status']} | "
                  f"steps = {result['steps']}, "
                  f"cycle_length = {result['cycle_length']}")

    print("🎉 All simulations complete. Transitions saved to:", output_file)
