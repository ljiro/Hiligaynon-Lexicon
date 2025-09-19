import pandas as pd
from pathlib import Path

# Input/output paths
csv_input = Path(r"C:\Users\CODE CLASSES\nlp\Hiligaynon-Lexicon\output\preprocessed-output\Lexicon_merged.csv")
txt_input = Path(r"C:\Users\CODE CLASSES\nlp\Hiligaynon-Lexicon\output\vader-output\vader_hiligaynon_cleaned.txt")
output_path = Path(r"C:\Users\CODE CLASSES\nlp\Hiligaynon-Lexicon\output\Lexicon_merged_scores.csv")

# Load CSV
lexicon = pd.read_csv(csv_input)

# Load TXT (row order matters here)
scores = pd.read_csv(
    txt_input,
    sep="\t",
    header=None,
    names=["word", "score", "col3", "col4"]
)[["word", "score"]]

# Reset indexes to align rows properly
lexicon = lexicon.reset_index(drop=True)
scores = scores.reset_index(drop=True)

# Merge row by row (ignore word matching)
lexicon_with_scores = pd.concat([lexicon, scores["score"]], axis=1)

# Save
lexicon_with_scores.to_csv(output_path, index=False)

print(f"✅ Merged row-by-row with 'score' column added: {output_path}")
