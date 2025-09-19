import pandas as pd
import re

# Load CSV
df = pd.read_csv("hiligaynon_lexicon.csv")

# Keep a copy of rows to fill POS
rows = []
current_pos = ""

for _, row in df.iterrows():
    word = str(row["Word"])

    # Case 1: Category row → extract POS
    if word.startswith("Category:Hiligaynon"):
        match = re.search(r"Hiligaynon (.+)", word)
        if match:
            # take the last word (noun, verb, adjective, etc.)
            pos_candidate = match.group(1).split()[-1].rstrip("s").lower()
            current_pos = pos_candidate
        continue  # don't keep category rows

    # Case 2: Normal word → assign POS if missing
    if pd.isna(row["Part of speech"]) or row["Part of speech"] == "":
        row["Part of speech"] = current_pos

    rows.append(row)

# Create cleaned DataFrame
cleaned_df = pd.DataFrame(rows)

# Save
cleaned_df.to_csv("hiligaynon_lexicon_with_pos.csv", index=False, encoding="utf-8")
print("✅ Cleaned CSV saved with correct POS!")