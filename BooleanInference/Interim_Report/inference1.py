import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree

# --- Load transition data ---
df = pd.read_csv("state_transitions.csv")

# --- Convert bitstrings to binary arrays ---
def unpack_bits(s):
    return [int(bit) for bit in s]

X = df["from_state"].apply(unpack_bits)
Y = df["to_state"].apply(unpack_bits)

num_genes = len(X[0])
gene_names = [f"G{i}" for i in range(num_genes)]

X = pd.DataFrame(X.tolist(), columns=gene_names)
Y = pd.DataFrame(Y.tolist(), columns=gene_names)

# --- Extract Boolean rule from decision tree ---
def extract_rule(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    paths = []

    def recurse(node, expr):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            left_expr = expr + [f"NOT {name}"]
            right_expr = expr + [name]
            recurse(tree_.children_left[node], left_expr)
            recurse(tree_.children_right[node], right_expr)
        else:
            val = tree_.value[node][0]
            if len(val) == 1:
                class_val = 0
            else:
                class_val = int(val[1] > val[0])
            if class_val == 1:
                paths.append(expr)

    recurse(0, [])

    if not paths:
        return "0"  # always off
    return " OR ".join(["(" + " AND ".join(path) + ")" for path in paths])

# --- Train a tree and extract rule for each gene ---
print("\n🧠 Inferred Boolean Network:\n")
for gene in gene_names:
    clf = DecisionTreeClassifier(max_leaf_nodes=10, random_state=0)
    clf.fit(X, Y[gene])
    rule = extract_rule(clf, gene_names)
    print(f"{gene} = {rule}")
