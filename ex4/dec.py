import math
import csv

def calculate_entropy(labels, context=""):
    total_count = len(labels)
    if total_count == 0:
        return 0

    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1

    entropy = 0
    probs_str = []
    for label, count in counts.items():
        prob = count / total_count
        entropy -= prob * math.log2(prob)
        probs_str.append(f"P({label})={count}/{total_count}")

    if context:
        print(f"    {context:<20} | Entropy: {entropy:.4f} | Dist: {', '.join(probs_str)}")

    return entropy
def print_frequency_table(data, feature_name, col_i, target_index):
    unique_vals = sorted(set(row[col_i] for row in data))
    target_labels = sorted(set(row[target_index] for row in data))
    header = f"| {feature_name:<12} | " + " | ".join(f"{str(l):<5}" for l in target_labels) + " | Total |"
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    for val in unique_vals:
        row_counts = []
        total = 0
        for label in target_labels:
            count = len([row for row in data if row[col_i] == val and row[target_index] == label])
            row_counts.append(count)
            total += count

        row_str = f"| {val:<12} | " + " | ".join(f"{c:<5}" for c in row_counts) + f" | {total:<5} |"
        print(row_str)
    print("-" * len(header) + "\n")

def draw_tree_step(data, headers, indent=""):
    target_index = len(headers) - 1
    labels = [row[target_index] for row in data]

    if len(set(labels)) == 1:
        return f" -> Leaf: {labels[0]}"

    if len(headers) == 1:
        majority = max(set(labels), key=labels.count)
        return f" -> Leaf (Majority): {majority}"

    best_gain = -1
    best_feat_idx = 0
    total_ent = calculate_entropy(labels)

    for i in range(len(headers) - 1):
        unique_vals = set(row[i] for row in data)
        w_entropy = 0
        for val in unique_vals:
            subset = [row[target_index] for row in data if row[i] == val]
            w_entropy += (len(subset) / len(data)) * calculate_entropy(subset)

        gain = total_ent - w_entropy
        if gain > best_gain:
            best_gain, best_feat_idx = gain, i

    feature_name = headers[best_feat_idx]
    tree_output = f"\n{indent}[{feature_name}?]"

    unique_vals = sorted(set(row[best_feat_idx] for row in data))
    for val in unique_vals:
        sub_data = [row[:best_feat_idx] + row[best_feat_idx+1:] for row in data if row[best_feat_idx] == val]
        sub_headers = headers[:best_feat_idx] + headers[best_feat_idx+1:]
        path = draw_tree_step(sub_data, sub_headers, indent + "    ")
        tree_output += f"\n{indent}  +-- {val}{path}"

    return tree_output

def process_decision_tree(filename):
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            data = list(reader)

        target_index = len(headers) - 1
        target_labels = [row[target_index] for row in data]

        print(f"\n--- STEP 1: OVERALL SYSTEM ENTROPY ---")
        total_entropy = calculate_entropy(target_labels, context="Total Entropy")
        print(f"Total Entropy [H(S)]: {total_entropy:.4f}\n")

        print(f"--- STEP 2: FREQUENCY TABLES & FEATURE CALCULATIONS ---")
        best_gain = -1
        root_node = ""

        for col_i in range(len(headers) - 1):
            feature_name = headers[col_i]
            print_frequency_table(data, feature_name, col_i, target_index)
            print(f"Entropy Analysis for: {feature_name}")
            feature_values = [row[col_i] for row in data]
            unique_vals = set(feature_values)
            weighted_entropy = 0
            for val in unique_vals:
                subset = [data[i][target_index] for i in range(len(data)) if data[i][col_i] == val]
                weight = len(subset) / len(data)
                sub_entropy = calculate_entropy(subset, context=f"Value: {val}")
                weighted_entropy += weight * sub_entropy

            gain = total_entropy - weighted_entropy
            print(f"  > Weighted Child Entropy: {weighted_entropy:.4f}")
            print(f"  > Information Gain: {gain:.4f}\n")

            if gain > best_gain:
                best_gain = gain
                root_node = feature_name

        print(f"--- STEP 3: TREE ILLUSTRATION ---")
        print("Constructing path from Root Node...")
        print(draw_tree_step(data, headers))

        print(f"\n--- FINAL DECISION ---")
        print(f"The Root Node is '{root_node}' with the highest Information Gain of {best_gain:.4f}.")

    except FileNotFoundError:
        print(f"File '{filename}' not found. Please ensure 'data.csv' exists.")

if __name__ == "__main__":
    process_decision_tree('data.csv')
