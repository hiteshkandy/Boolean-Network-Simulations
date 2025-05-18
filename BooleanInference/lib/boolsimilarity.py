import re
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    matthews_corrcoef, roc_auc_score, average_precision_score
)

def parse_network(text):
    """
    Parse a Boolean network in “vX = …” text form and
    return (set of edges, set of all variables).
    An edge (u,v) means u appears (negated or not) in v’s update.
    """
    edges = set()
    vars_ = set()
    for line in text.strip().splitlines():
        if not line.strip(): continue
        lhs, rhs = line.split('=', 1)
        target = lhs.strip()
        vars_.add(target)
        # find all variable tokens v0, v1, … in the right-hand side
        regs = re.findall(r'\b(v\d+)\b', rhs)
        for u in regs:
            vars_.add(u)
            edges.add((u, target))
    return edges, vars_

def compute_edge_metrics(gt_text, pred_text):
    """
    Given ground-truth and predicted networks (text form),
    compute precision, recall, F1, MCC, AUROC, and AUPR.
    """
    gt_edges, vars1 = parse_network(gt_text)
    pred_edges, vars2 = parse_network(pred_text)
    variables = sorted(vars1.union(vars2))

    # build the full list of possible directed edges (including self-loops)
    all_edges = [(u, v) for u in variables for v in variables]

    # binary labels for each possible edge
    y_true = [1 if e in gt_edges   else 0 for e in all_edges]
    y_pred = [1 if e in pred_edges else 0 for e in all_edges]

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall    = recall_score(y_true, y_pred, zero_division=0)
    f1        = f1_score(y_true, y_pred, zero_division=0)
    mcc       = matthews_corrcoef(y_true, y_pred)

    # treat the 0/1 predictions as “scores” for AUROC/AUPR
    auroc = roc_auc_score(y_true, y_pred)
    aupr  = average_precision_score(y_true, y_pred)

    return {
        'precision': precision,
        'recall':    recall,
        'f1_score':  f1,
        'mcc':       mcc,
        'auroc':     auroc,
        'aupr':      aupr
    }

if __name__ == '__main__':
    gt_network = '''v0 = v1 AND NOT v2
v1 = v0 OR v3
v2 = NOT v4
v3 = v2 OR NOT v5
v4 = v3 AND v6
v5 = NOT v1 OR v4
v6 = v5 AND NOT v0'''

    mibni_network = '''v0 = v3 AND NOT v3
v1 = 1
v2 = NOT v0 AND v3
v3 = NOT v0 OR v5
v4 = v6
v5 = NOT v3 AND v3
v6 = v4'''

    metrics = compute_edge_metrics(gt_network, mibni_network)
    print("Edge-recovery metrics:")
    for name, val in metrics.items():
        print(f"  {name:6s}: {val:.4f}")
