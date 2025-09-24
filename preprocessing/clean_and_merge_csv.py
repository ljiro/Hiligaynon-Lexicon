import pandas as pd
import unicodedata
from pathlib import Path

# === File paths ===
base_dir = Path(r"C:\Users\CODE CLASSES\nlp\Hiligaynon-Lexicon\output\preprocessed-output")
cec_file = base_dir / "NLP Lexicon - Cecielmotus.csv"
wiki_file = base_dir / "NLP Lexicon - Wikitionary.csv"

cec_cleaned = base_dir / "Cecielmotus_cleaned.csv"
wiki_cleaned = base_dir / "Wikitionary_cleaned.csv"
merged_file = base_dir / "Ceciel_Wiki_merged.csv"
excluded_file = base_dir / "excluded_expressions.csv"

# === Penn Treebank POS Mapping ===
pos_map = {
    "noun": "NN",
    "noun formative": "NN",
    "verb": "VB",
    "verbal affix": "VB",
    "adjective": "JJ",
    "adjective formative": "JJ",
    "adverb": "RB",
    "pronoun": "PRP",
    "particle": "RP",
    "conjunction": "CC",
    "interjection": "UH",
    "numeral": "CD",
    "determiner": "DT",
    "deictic": "DT",
}

drop_categories = {"phrase", "idiom", "phrasebook"}


# === Utility: Normalize word (for grouping only) ===
def normalize_word(word: str) -> str:
    if not isinstance(word, str):
        return ""
    return "".join(
        c for c in unicodedata.normalize("NFD", word) if unicodedata.category(c) != "Mn"
    ).lower()


# === Function to clean a dataset ===
def clean_dataset(path, rename_map=None):
    df = pd.read_csv(path, dtype=str)

    # Rename if needed
    if rename_map:
        df = df.rename(columns=rename_map)

    # Keep only the important columns
    keep_cols = ["word", "POS word", "meaning"]
    df = df[[c for c in keep_cols if c in df.columns]]

    # Normalize text
    df = df.apply(lambda col: col.astype(str).str.strip().str.lower())

    # Forward-fill missing words
    if "word" in df.columns:
        df["word"] = df["word"].replace("nan", pd.NA).ffill()

    # Drop excluded categories
    excluded = pd.DataFrame()
    if "POS word" in df.columns:
        excluded = df[df["POS word"].isin(drop_categories)]
        df = df[~df["POS word"].isin(drop_categories)]

    # Map POS word → Penn Treebank symbol
    df["POS symbol"] = df["POS word"].map(pos_map)

    # Reorder columns
    df = df[["word", "POS symbol", "POS word", "meaning"]]

    return df, excluded


# === Process Cecielmotus ===
cec_df, cec_excluded = clean_dataset(cec_file)
cec_df.to_csv(cec_cleaned, index=False)

# === Process Wiktionary ===
wiki_df, wiki_excluded = clean_dataset(
    wiki_file, rename_map={"Part of speech": "POS word", "Word": "word"}
)
wiki_df.to_csv(wiki_cleaned, index=False)

# === Save excluded rows ===
excluded_all = pd.concat([cec_excluded, wiki_excluded], ignore_index=True)
excluded_all.to_csv(excluded_file, index=False)

# === Merge both datasets ===
merged = pd.concat([cec_df, wiki_df], ignore_index=True)

# Add normalized form for grouping
merged["group"] = merged["word"].apply(normalize_word)

# Sort so that variants (like "tubig" and "túbig") appear together
merged = merged.sort_values(by=["group", "word"]).reset_index(drop=True)

# Drop rows with blank meaning
merged = merged[merged["meaning"].notna() & (merged["meaning"].str.strip() != "")]

# Save merged file (without "group" helper column)
merged.drop(columns=["group"], inplace=True)
merged.to_csv(merged_file, index=False)

# === Report ===
print("=== Cleaning Report ===")
print(f"Cecielmotus rows: {cec_df.shape[0]}")
print(f"Wikitionary rows: {wiki_df.shape[0]}")
print(f"Excluded rows saved: {excluded_all.shape[0]}")
print(f"Final merged rows: {merged.shape[0]}")
