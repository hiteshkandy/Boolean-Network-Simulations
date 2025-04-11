import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

# Load transition data
df = pd.read_csv("state_transitions.csv")

# Get number of genes from bitstring length
num_genes = len(df["from_state"][0])
gene_names = [f"G{i}" for i in range(num_genes)]

# Convert binary strings to lists of integers
def unpack_bits(s):
    return [int(bit) for bit in s]

X = df["from_state"].apply(unpack_bits)
Y = df["to_state"].apply(unpack_bits)

X = pd.DataFrame(X.tolist(), columns=gene_names)
Y = pd.DataFrame(Y.tolist(), columns=gene_names)

# Train decision tree per gene
for gene in gene_names:
    y = Y[gene]
    clf = DecisionTreeClassifier(max_leaf_nodes=10, random_state=0)
    clf.fit(X, y)

    print(f"\n🧠 Boolean rule for {gene}:")
    print(export_text(clf, feature_names=gene_names))
