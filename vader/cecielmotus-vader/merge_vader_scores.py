import pandas as pd
from pathlib import Path

# Input/output paths
csv_input = Path(r"/output/preprocessed-output\Lexicon_merged.csv")
txt_input = Path(r"/output/vader-output/vader_hiligaynon_cleaned.txt")
output_path = Path(r"C:\Users\CODE CLASSES\nlp\Hiligaynon-Lexicon\output\Lexicon_merged_scores.csv")

# Load CSV
lexicon = pd.read_csv(csv_input)

# Load TXT (word + score only)
scores = pd.read_csv(
    txt_input,
    sep="\t",
    header=None,
    names=["word", "score", "col3", "col4"]
)[["word", "score"]]

# Drop duplicate words
scores = scores.drop_duplicates(subset=["word"], keep="first")

# Merge
lexicon_with_scores = (
    lexicon.drop(columns=["score"], errors="ignore")
           .merge(scores, on="word", how="left")
)

# Save 
lexicon_with_scores.to_csv(output_path, index=False)

print(f"✅ Merged with single 'score' column: {output_path}")
