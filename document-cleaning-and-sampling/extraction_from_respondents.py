import pandas as pd
from pathlib import Path

# === File paths ===
base_path = Path(r"C:\Users\CODE CLASSES\nlp\Hiligaynon-Lexicon\output")
full_file = base_path / "respondents" / "NLP Lexicon - Merged_csv_with_scores_with_respondents.csv"
sample_file = base_path / "stratified_sample.csv"
output_file = base_path / "NLP_Lexicon_Sampled_with_Respondents.csv"

# === Columns to match on ===
KEY_COLUMNS = ["word", "pos_symbol", "pos_word", "meaning", "sentiment score", "sentiment"]

# === Load CSVs ===
df_full = pd.read_csv(full_file)
df_sample = pd.read_csv(sample_file)

# === Filter rows by multiple keys ===
df_merged = df_full.merge(df_sample[KEY_COLUMNS], on=KEY_COLUMNS, how="inner")

# === Save output ===
df_merged.to_csv(output_file, index=False)

print(f"✅ Sample with respondents' answers saved to:\n{output_file}")
print(f"📊 Rows in sample: {len(df_merged)}")
