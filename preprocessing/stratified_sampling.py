import os
import pandas as pd
import numpy as np

# Get input/output paths
input_csv = r"C:\Users\CODE CLASSES\nlp\Hiligaynon-Lexicon\output\Ceciel_Wiki_merged_scores.csv"
output_dir = os.path.dirname(input_csv)
output_csv = os.path.join(output_dir, "stratified_sample.csv")

df = pd.read_csv(input_csv)
N = len(df)   # should be 6478
stratum_col = "sentiment"
n_total = 363

# stratum sizes
counts = df[stratum_col].value_counts().sort_index()

# proportional allocation
alloc = (counts / counts.sum() * n_total).round().astype(int)

# adjust rounding so sum equals n_total
diff = n_total - alloc.sum()
if diff != 0:
    order = alloc.sort_values(ascending=False).index if diff > 0 else alloc.sort_values().index
    i = 0
    while diff != 0:
        idx = order[i % len(order)]
        alloc[idx] += 1 if diff > 0 else -1
        diff += -1 if diff > 0 else 1
        i += 1

# draw sample within each stratum
sampled = []
rng = np.random.default_rng(42)
for s, n_i in alloc.items():
    if n_i <= 0:
        continue
    group = df[df[stratum_col] == s]
    sampled.append(group.sample(n=n_i, random_state=int(rng.integers(1_000_000))))

sample_df = pd.concat(sampled, ignore_index=True)

# Save in the same folder as the input file
sample_df.to_csv(output_csv, index=False)
print(f"Sample created: {len(sample_df)} rows")
print(f"Saved to: {output_csv}")
